from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.urls import reverse
from jose import jwt
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Course, Department, User
from .utils import hash_password


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.password = "safe-password-123"
        self.user = User.objects.create(
            username="learner",
            email="learner@example.com",
            password=hash_password(self.password),
        )
        self.department = Department.objects.create(
            name="Engineering", head_of_dept="Priya", budget="100000.00"
        )
        self.course = Course.objects.create(
            name="Python", code="PY101", credits=4, department=self.department
        )

    def login(self):
        response = self.client.post(
            reverse("jwt-login"),
            {"email": self.user.email, "password": self.password},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data["access_token"]

    def test_login_returns_bearer_token_with_30_minute_expiry(self):
        before_login = datetime.now(timezone.utc)
        response = self.client.post(
            reverse("jwt-login"),
            {"email": self.user.email, "password": self.password},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["token_type"], "bearer")
        payload = jwt.decode(
            response.data["access_token"],
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        expiry = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        self.assertEqual(payload["sub"], self.user.email)
        self.assertAlmostEqual(
            (expiry - before_login).total_seconds(), 30 * 60, delta=2
        )

    def test_course_list_is_public(self):
        response = self.client.get("/api/v1/courses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_create_requires_authentication(self):
        response = self.client.post(
            "/api/v1/courses/",
            {
                "name": "Django",
                "code": "DJ101",
                "credits": 4,
                "department": self.department.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_and_delete_course(self):
        token = self.login()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        create_response = self.client.post(
            "/api/v1/courses/",
            {
                "name": "Django",
                "code": "DJ101",
                "credits": 4,
                "department": self.department.id,
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        delete_response = self.client.delete(f"/api/v1/courses/{self.course.id}/")
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_expired_token_is_rejected(self):
        expired_token = jwt.encode(
            {
                "sub": self.user.email,
                "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
            },
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {expired_token}")

        response = self.client.delete(f"/api/v1/courses/{self.course.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cors_allows_frontend_origin(self):
        response = self.client.options(
            "/api/v1/courses/",
            HTTP_ORIGIN="http://localhost:3000",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="POST",
        )
        self.assertEqual(
            response.headers.get("access-control-allow-origin"),
            "http://localhost:3000",
        )
