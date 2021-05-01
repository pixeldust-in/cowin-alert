from django.utils import timezone

from core.models import AlertRequest


def run_fetcher():
    alert_requests = (
        AlertRequest.objects.filter(
            from_date__gte=timezone.localdate(), to_date__gte=timezone.localdate()
        )
        .order_by()
        .values_list("pincode", flat=True)
        .distinct()
    )
    # Get all requests where start_date >= today =<enddate
    # get unique pincodes
    # make request to COWIN API for date & pincode
    # store recieved data in models
    # trigger notification sending function


def trigger_alert():
    pass
    # session query for today
    # get session date & pincodes
    # query in alert for pincodes
