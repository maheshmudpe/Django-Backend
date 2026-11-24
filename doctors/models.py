
import uuid

from django.db import models


class Doctor(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    full_name = models.CharField(max_length=150)

    specialization = models.CharField(max_length=100)

    email = models.EmailField(
        blank=True,
        null=True
    )

    phone = models.CharField(max_length=20)

    qualification = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    experience_years = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
