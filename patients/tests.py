
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Patient

User = get_user_model()


class PatientAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            name="Test User",
            email="test@example.com",
            password="StrongPass!9284",
        )

        self.other_user = User.objects.create_user(
            name="Other User",
            email="other@example.com",
            password="StrongPass!9284",
        )

        self.client.force_authenticate(user=self.user)

        self.patient_data = {
            "full_name": "John Doe",
            "date_of_birth": "1995-05-15",
            "gender": "MALE",
            "phone": "9876543210",
            "address": "Pune",
            "medical_notes": "No known allergies",
        }

    def create_patient(self, user=None):
        return Patient.objects.create(
            created_by=user or self.user,
            **self.patient_data
        )

    def test_create_patient_success(self):
        response = self.client.post(
            reverse("patient-list-create"),
            self.patient_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(Patient.objects.first().created_by, self.user)

    def test_list_only_own_patients(self):
        self.create_patient(self.user)
        self.create_patient(self.other_user)

        response = self.client.get(reverse("patient-list-create"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_own_patient(self):
        patient = self.create_patient()

        response = self.client.get(
            reverse("patient-detail", kwargs={"pk": patient.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_retrieve_another_users_patient(self):
        patient = self.create_patient(self.other_user)

        response = self.client.get(
            reverse("patient-detail", kwargs={"pk": patient.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_own_patient(self):
        patient = self.create_patient()

        response = self.client.put(
            reverse("patient-detail", kwargs={"pk": patient.pk}),
            {
                **self.patient_data,
                "full_name": "Updated Name",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        patient.refresh_from_db()
        self.assertEqual(patient.full_name, "Updated Name")

    def test_delete_own_patient(self):
        patient = self.create_patient()

        response = self.client.delete(
            reverse("patient-detail", kwargs={"pk": patient.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Patient.objects.filter(pk=patient.pk).exists())

    def test_cannot_delete_another_users_patient(self):
        patient = self.create_patient(self.other_user)

        response = self.client.delete(
            reverse("patient-detail", kwargs={"pk": patient.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Patient.objects.filter(pk=patient.pk).exists())

    def test_unauthenticated_user_cannot_list_patients(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(reverse("patient-list-create"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
