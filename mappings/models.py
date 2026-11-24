
import uuid

from django.db import models


class Mapping(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="doctor_mappings"
    )

    doctor = models.ForeignKey(
        "doctors.Doctor",
        on_delete=models.PROTECT,
        related_name="patient_mappings"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["patient", "doctor"],
                name="unique_patient_doctor_mapping"
            )
        ]

    def __str__(self):
        return f"{self.patient.full_name} - {self.doctor.full_name}"
