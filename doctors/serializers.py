
from rest_framework import serializers

from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor

        fields = [
            "id",
            "full_name",
            "specialization",
            "email",
            "phone",
            "qualification",
            "experience_years",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
