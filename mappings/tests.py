
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from patients.models import Patient
from doctors.models import Doctor
from .models import Mapping

User = get_user_model()


class MappingAPITests(APITestCase):

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

        self.patient = Patient.objects.create(
            full_name="John Doe",
            date_of_birth="1995-05-15",
            gender="MALE",
            phone="9876543210",
            created_by=self.user,
        )

        self.other_patient = Patient.objects.create(
            full_name="Jane Doe",
            date_of_birth="1998-08-20",
            gender="FEMALE",
            phone="9876543211",
            created_by=self.other_user,
        )

        self.doctor = Doctor.objects.create(
            full_name="Dr. Smith",
            specialization="Cardiology",
            phone="9876543212",
        )

    def create_mapping(self, patient=None):
        return Mapping.objects.create(
            patient=patient or self.patient,
            doctor=self.doctor,
        )

    def test_create_mapping_success(self):
        response = self.client.post(
            reverse("mapping-list-create"),
            {
                "patient": str(self.patient.id),
                "doctor": str(self.doctor.id),
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mapping.objects.count(), 1)

    def test_list_only_own_patient_mappings(self):
        self.create_mapping(self.patient)
        self.create_mapping(self.other_patient)

        response = self.client.get(reverse("mapping-list-create"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_mappings_for_own_patient(self):
        self.create_mapping()

        response = self.client.get(
            reverse(
                "patient-mappings",
                kwargs={"patient_id": self.patient.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_cannot_list_another_users_patient_mappings(self):
        self.create_mapping(self.other_patient)

        response = self.client.get(
            reverse(
                "patient-mappings",
                kwargs={"patient_id": self.other_patient.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_duplicate_mapping_is_rejected(self):
        self.create_mapping()

        response = self.client.post(
            reverse("mapping-list-create"),
            {
                "patient": str(self.patient.id),
                "doctor": str(self.doctor.id),
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Mapping.objects.count(), 1)

    def test_cannot_assign_doctor_to_another_users_patient(self):
        response = self.client.post(
            reverse("mapping-list-create"),
            {
                "patient": str(self.other_patient.id),
                "doctor": str(self.doctor.id),
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Mapping.objects.count(), 0)

    def test_delete_own_mapping(self):
        mapping = self.create_mapping()

        response = self.client.delete(
            reverse(
                "mapping-delete",
                kwargs={"mapping_id": mapping.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Mapping.objects.filter(id=mapping.id).exists())

    def test_cannot_delete_another_users_mapping(self):
        mapping = self.create_mapping(self.other_patient)

        response = self.client.delete(
            reverse(
                "mapping-delete",
                kwargs={"mapping_id": mapping.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Mapping.objects.filter(id=mapping.id).exists())

    def test_unauthenticated_user_cannot_list_mappings(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(reverse("mapping-list-create"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
