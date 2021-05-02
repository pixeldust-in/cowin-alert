from celery.utils.log import get_task_logger
from django.contrib.sites.models import Site
from django.utils import timezone
from glom import glom

from celery_app import app
from core import email, serializers
from core.models import AlertRequest, CowinCenter, CowinSession, SessionAlertMap
from core.services.cowin import CowinApi

logger = get_task_logger(__name__)


def build_domain_url(path=None):
    url = f"https://{Site.objects.get_current().domain}"
    if not path:
        return f"{url}/"
    return f"{url}{path}"


def save_sessions(center_id, sessions):
    sessions_ids = []
    for session in sessions:
        if session["available_capacity"] > 0:
            session_id = session["session_id"]
            data = {
                **session,
                "date": timezone.datetime.strptime(session["date"], "%d-%m-%Y").date(),
                "center": CowinCenter.objects.get(center_id=center_id).id,
            }
            try:
                CowinSession.objects.get(session_id=session_id)
            except CowinSession.DoesNotExist:
                session_serializer = serializers.CowinSessionSerializer(data=data)
                session_serializer.is_valid(raise_exception=True)
                session_serializer.save()

            sessions_ids.append(session_id)

    return sessions_ids


@app.task(bind=True, retry_kwargs={"max_retries": 2})
def fetch_cowin(self):
    today = timezone.localdate()
    pincodes = (
        AlertRequest.objects.filter(
            from_date__lte=today, to_date__gte=today, alerts_enabled=True
        )
        .order_by()
        .values_list("pincode", flat=True)
        .distinct()
    )
    logger.info(f"{pincodes.count()} unique pincode found")
    for pincode in pincodes:
        reponse = CowinApi.search_by_pincode(
            pincode=pincode, date=today.strftime("%d-%m-%Y")
        )
        logger.info("API reponse recieved for pincode %s", pincode)

        data = reponse.json()
        centers = glom(data, "centers", default=[])

        created_session_ids = []

        if centers:
            logger.info(f"{len(centers)} centers found for pincode {pincode}")
            # First we save centers then save sessions
            for center in centers:
                try:
                    CowinCenter.objects.get(center_id=center["center_id"])
                except CowinCenter.DoesNotExist:
                    serializer = serializers.CowinCenterSerializer(data=center)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                session_ids = save_sessions(center["center_id"], center["sessions"])
                created_session_ids.extend(session_ids)

        # we have pincode session
        sessions = CowinSession.objects.filter(session_id__in=created_session_ids)
        if sessions.exists():
            minimum_age = min([int(session.min_age_limit) for session in sessions])
            alert_requests = AlertRequest.objects.filter(
                pincode=pincode,
                from_date__lte=today,
                to_date__gte=today,
                age__gte=minimum_age,
                alerts_enabled=True,
            )
            if alert_requests.exists():
                qualifying_alert_ids = [item.id for item in alert_requests]
                send_alert.delay(qualifying_alert_ids, created_session_ids)


@app.task(bind=True, retry_kwargs={"max_retries": 2})
def send_alert(self, qualifying_alert_ids, session_ids):
    logger.info(f"send_alert {qualifying_alert_ids} {session_ids}")

    alert_requests = AlertRequest.objects.filter(id__in=qualifying_alert_ids)
    sessions = CowinSession.objects.filter(session_id__in=session_ids)
    for alert_req in alert_requests:
        pincode = alert_req.pincode
        session_ids_already_notified = [
            item.session_id
            for item in SessionAlertMap.objects.filter(alert_request_id=alert_req.id)
        ]
        matching_sessions = sessions.filter(
            center__pincode=pincode,
        ).exclude(id__in=session_ids_already_notified)
        if matching_sessions.exists():
            context = {
                "alert_request": alert_req,
                "sessions": matching_sessions,
                "unsubscribe_url": build_domain_url(alert_req.get_unsubscribe_url()),
            }
            email.send_mass_individual_mail(
                recipient_list=[alert_req.email],
                subject=f"New CoWin session available for pincode {pincode}",
                context=context,
                template="email/session_available_alert.html",
            )
            SessionAlertMap.objects.bulk_create(
                [
                    SessionAlertMap(
                        session_id=session.id, alert_request_id=alert_req.id
                    )
                    for session in matching_sessions
                ]
            )
