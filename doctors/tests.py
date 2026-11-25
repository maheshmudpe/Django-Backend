
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Doctor

User = get_user_model()


class DoctorAPITests(APITestCase):

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

        self.doctor_data = {
            "full_name": "Dr. John Smith",
            "specialization": "Cardiology",
            "email": "doctor@example.com",
            "phone": "9876543210",
            "qualification": "MBBS, MD",
            "experience_years": 10,
        }

    def create_doctor(self):
        return Doctor.objects.create(**self.doctor_data)

    def test_create_doctor_success(self):
        response = self.client.post(
            reverse("doctor-list-create"),
            self.doctor_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Doctor.objects.count(), 1)

    def test_list_doctors(self):
        self.create_doctor()

        response = self.client.get(reverse("doctor-list-create"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_doctor(self):
        doctor = self.create_doctor()

        response = self.client.get(
            reverse("doctor-detail", kwargs={"pk": doctor.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_doctor(self):
        doctor = self.create_doctor()

        response = self.client.put(
            reverse("doctor-detail", kwargs={"pk": doctor.pk}),
            {
                **self.doctor_data,
                "full_name": "Dr. Updated Name",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        doctor.refresh_from_db()
        self.assertEqual(doctor.full_name, "Dr. Updated Name")

    def test_delete_doctor(self):
        doctor = self.create_doctor()

        response = self.client.delete(
            reverse("doctor-detail", kwargs={"pk": doctor.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Doctor.objects.filter(pk=doctor.pk).exists())

    def test_another_authenticated_user_can_view_shared_doctor(self):
        doctor = self.create_doctor()

        self.client.force_authenticate(user=self.other_user)

        response = self.client.get(
            reverse("doctor-detail", kwargs={"pk": doctor.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_cannot_list_doctors(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(reverse("doctor-list-create"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
