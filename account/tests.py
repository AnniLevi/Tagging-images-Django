from json import dumps

from django.contrib.auth.models import User
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.permissions import check_user_group


class AccountTests(APITestCase):
    def setUp(self):
        call_command("creategroups")

    def test_create_account(self):
        """Ensure we can create a new user object."""
        url = reverse("auth_register")

        # GOOD CASE
        data = {
            "username": "APITestUser",
            "first_name": "APITestUser",
            "last_name": "APITestUser",
            "email": "apitest@test.test",
            "password": "useruser123",
        }
        response = self.client.post(
            url, data=dumps(data), content_type="application/json"
        )
        # check status msg 201
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg=response.data
        )
        self.assertEqual(response.data["username"], data["username"])
        # check creating user obj
        user = User.objects.get(username=response.data["username"])
        self.assertEqual(response.data["username"], user.username)
        # check user group
        check_user_group(user, [0])

        # BAD CASE
        response2 = self.client.post(
            url, data=dumps(data), content_type="application/json"
        )
        # 400 - unique username failed
        self.assertEqual(
            response2.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data
        )
