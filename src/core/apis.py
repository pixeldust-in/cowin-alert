from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import AlertRequest

from .serializers import AlertRequestSerializer


@api_view(["POST"])
@csrf_exempt
def alert_registrations(request):
    data = request.data
    serializer = AlertRequestSerializer(data=data)
    if not serializer.is_valid(raise_exception=True):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(status=status.HTTP_201_CREATED)


@csrf_exempt
def unsubscribe(request, uuid):
    alert_obj = get_object_or_404(AlertRequest, uuid=uuid)
    alert_obj.unsubscribe()
    additional_entries = AlertRequest.objects.filter(
        email=alert_obj.email, alerts_enabled=True
    )
    if additional_entries.exists():
        for entry in additional_entries:
            entry.unsubscribe()
    return render(request, "unsubscribed.html")
