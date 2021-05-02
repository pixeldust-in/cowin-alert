from rest_framework import serializers

from . import models


class CowinCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CowinCenter
        fields = (
            "id",
            "center_id",
            "pincode",
            "name",
            "state_name",
            "district_name",
            "block_name",
        )


class CowinSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CowinSession
        fields = (
            "center",
            "session_id",
            "date",
            "available_capacity",
            "min_age_limit",
            "vaccine",
            "slots",
        )


class AlertRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AlertRequest
        fields = (
            "email",
            "from_date",
            "to_date",
            "age",
            "pincode",
        )
