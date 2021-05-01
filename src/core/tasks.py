from celery.utils.log import get_task_logger
from django.utils import timezone
from glom import glom

from celery_app import app
from core import serializers
from core.models import AlertRequest, CowinCenter, CowinSession
from core.services.cowin import CowinApi

logger = get_task_logger(__name__)


def save_sessions(center_id, sessions):
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


@app.task(bind=True, retry_kwargs={"max_retries": 2})
def fetch_cowin(self):
    today = timezone.localdate()
    pincodes = (
        AlertRequest.objects.filter(from_date__lte=today, to_date__gte=today)
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

                save_sessions(center["center_id"], center["sessions"])


@app.task(bind=True, retry_kwargs={"max_retries": 2})
def trigger_alert(self, alert_id, session_id):
    logger.info("Starting trigger_alert for %s task %s", alert_id, session_id)


@app.task(bind=True, retry_kwargs={"max_retries": 2})
def handle_session_create(self, session_id):
    # TODO: figure out login of how to club and send a single alert and not multiple alerts
    session = CowinSession.objects.get(id=session_id)
    matched_alert_requests = AlertRequest.objects.filter(
        pincode=session.center.pincode,
        from_date__lte=session.date,
        to_date__gte=session.date,
        age__gte=session.min_age_limit,
    )
    if matched_alert_requests.exists():
        for alert in matched_alert_requests:
            trigger_alert.delay(alert.id, session_id)
