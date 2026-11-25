
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

User = get_user_model()


class AuthenticationTests(APITestCase):

    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")

        self.user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "StrongPass!9284",
        }

    def test_user_registration_success(self):
        response = self.client.post(
            self.register_url,
            self.user_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            User.objects.filter(email="test@example.com").exists()
        )

    def test_password_is_hashed(self):
        self.client.post(
            self.register_url,
            self.user_data,
            format="json"
        )

        user = User.objects.get(email="test@example.com")

        self.assertNotEqual(user.password, self.user_data["password"])
        self.assertTrue(user.check_password(self.user_data["password"]))

    def test_duplicate_email_registration_fails(self):
        User.objects.create_user(**self.user_data)

        response = self.client.post(
            self.register_url,
            self.user_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self):
        User.objects.create_user(**self.user_data)

        response = self.client.post(
            self.login_url,
            {
                "email": self.user_data["email"],
                "password": self.user_data["password"],
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_with_invalid_password_fails(self):
        User.objects.create_user(**self.user_data)

        response = self.client.post(
            self.login_url,
            {
                "email": self.user_data["email"],
                "password": "WrongPassword123!",
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
