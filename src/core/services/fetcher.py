import logging

from django.utils import timezone
from glom import glom

from core import serializers
from core.models import AlertRequest, CowinCenter, CowinSession
from core.services.cowin import CowinApi

logger = logging.getLogger(__name__)


def run_fetcher():
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

        if not centers:
            return

        logger.info(f"{len(centers)} centers found for pincode {pincode}")
        # First we save centers then save sessions
        for center in centers:
            logger.info(f"{center}")

            try:
                CowinCenter.objects.get(center_id=center["center_id"])
            except CowinCenter.DoesNotExist:
                serializer = serializers.CowinCenterSerializer(data=center)
                serializer.is_valid(raise_exception=True)
                serializer.save()

            for session in center["sessions"]:
                session_id = session["session_id"]
                data = {
                    **session,
                    "date": timezone.datetime.strptime(
                        session["date"], "%d-%m-%Y"
                    ).date(),
                    "center": CowinCenter.objects.get(center_id=center["center_id"]).id,
                }
                try:
                    CowinSession.objects.get(session_id=session_id)
                except CowinSession.DoesNotExist:
                    session_serializer = serializers.CowinSessionSerializer(data=data)
                    session_serializer.is_valid(raise_exception=True)
                    session_serializer.save()


def trigger_alert():
    pass
    # session query for today
    # get session date & pincodes
    # query in alert for pincodes
