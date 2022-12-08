from json import dumps

from django.contrib.auth.models import Group, User
from django.core.files.images import ImageFile
from django.core.management import call_command
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.permissions import UserGroups
from images.models import Image, Tag


class ImageTests(APITestCase):
    def setUp(self):
        call_command("creategroups")
        usernames = ["user", "verif_user", "admin"]
        password = "testuser123"
        url = reverse("token_obtain_pair")
        users = []
        tokens = []
        for username, i in zip(usernames, range(3)):
            user = User.objects.create_user(username=username, password=password)
            user.groups.add(Group.objects.get(name=UserGroups(i).name))
            data = {"username": username, "password": password}
            response = self.client.post(
                url, data=dumps(data), content_type="application/json"
            )
            token = response.data["access"]
            users.append(user)
            tokens.append(token)

        self.user, self.verif_user, self.admin = users
        self.user_token, self.verif_user_token, self.admin_token = tokens

    @override_settings(
        CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
    )
    def test_image_view(self):
        """Ensure user can view images."""
        im = [
            Image(
                name="image1",
                img=ImageFile(
                    open("test_files/psichki.jpg", "rb"),
                    name=Image.create_image_name("image1"),
                ),
                user_id=1,
            )
            for _ in range(3)
        ]
        Image.objects.bulk_create(im)
        images = Image.objects.all()
        url = reverse("images")

        # bad case for anonymous user
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # good case for all roles
        for token in (self.user_token, self.verif_user_token, self.admin_token):
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, status.HTTP_200_OK, msg=response.data
            )
            self.assertEqual(response.data["count"], images.count())

    def test_image_create(self):
        """Ensure user can create a new single image."""
        url = reverse("images")

        # good case - for verified_user role
        data = {"name": "verif_user_image", "img": open("test_files/psichki.jpg", "rb")}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.verif_user_token}")
        response = self.client.post(url, data=data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg=response.data
        )
        self.assertEqual(response.data["user_id"], self.verif_user.id)
        image = Image.objects.get(id=response.data["id"])
        self.assertEqual(image.name, "verif_user_image")
        self.assertEqual(image.user_id, self.verif_user.id)

        # good case - for admin role
        data = {"name": "admin_image", "img": open("test_files/psichki.jpg", "rb")}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.post(url, data=data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg=response.data
        )
        self.assertEqual(response.data["user_id"], self.admin.id)
        image = Image.objects.get(id=response.data["id"])
        self.assertEqual(image.name, "admin_image")
        self.assertEqual(image.user_id, self.admin.id)

        # bad case - for user role
        data = {"name": "user_image", "img": open("test_files/psichki.jpg", "rb")}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.post(url, data=data)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data
        )
        self.assertFalse(Image.objects.filter(name="user_image").exists())

    def test_image_zip_create(self):
        """Ensure user can upload a zip archive with images."""
        url = reverse("upload_zip")

        # bad case - for user role
        data = {"zip_archive": open("test_files/new_ar.zip", "rb")}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.post(url, data=data)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data
        )
        self.assertFalse(Image.objects.exists())

        # good case - for verified_user and admin roles
        for user, token in zip(
            [self.verif_user, self.admin], [self.verif_user_token, self.admin_token]
        ):
            data = {"zip_archive": open("test_files/new_ar.zip", "rb")}
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
            response = self.client.post(url, data=data)
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, msg=response.data
            )
            self.assertTrue(Image.objects.exists())
            self.assertTrue(Image.objects.filter(user=user).exists())

    @override_settings(
        CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
    )
    def test_tags_view(self):
        """Ensure user can view tags."""
        im = Image.objects.create(
            name="image1",
            img=ImageFile(
                open("test_files/psichki.jpg", "rb"),
                name=Image.create_image_name("image1"),
            ),
            user_id=1,
        )
        im.tags.bulk_create(
            [
                Tag(tag="some words", user=user, img=im)
                for user in [self.user, self.verif_user, self.admin]
            ]
        )
        url = reverse("tags")

        # bad case for anonymous user
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # good case - all roles can see only their tags
        for user, token in zip(
            [self.user, self.verif_user, self.admin],
            [self.user_token, self.verif_user_token, self.admin_token],
        ):
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, status.HTTP_200_OK, msg=response.data
            )
            self.assertEqual(response.data["results"][0]["id"], user.id)

    def test_tags_create(self):
        """Ensure user can create tags."""
        im = Image.objects.create(
            name="image1",
            img=ImageFile(
                open("test_files/psichki.jpg", "rb"),
                name=Image.create_image_name("image1"),
            ),
            user_id=1,
        )
        url = reverse("tags")
        data = {"tag": "some words", "img_id": im.id}

        # bad case for anonymous user
        response = self.client.post(
            url, data=dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # good case - all roles can see only their tags
        for user, token in zip(
            [self.user, self.verif_user, self.admin],
            [self.user_token, self.verif_user_token, self.admin_token],
        ):
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
            response = self.client.post(url, data=data)
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, msg=response.data
            )
            self.assertTrue(im.tags.exists())
            self.assertTrue(im.tags.filter(user=user).exists())

    @override_settings(
        CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
    )
    def test_common_tags_and_most_tagged(self):
        """Ensure admin role can view common_tags and most_tagged."""
        im = Image.objects.create(
            name="image1",
            img=ImageFile(
                open("test_files/psichki.jpg", "rb"),
                name=Image.create_image_name("image1"),
            ),
            user_id=1,
        )
        im.tags.bulk_create(
            [
                Tag(tag="some words", user=user, img=im)
                for user in [self.user, self.verif_user, self.admin]
            ]
        )

        # bad case for anonymous user
        for u in ["common_tags", "most_tagged"]:
            response = self.client.get(reverse(u))
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # bad case for user and verified_user roles
        for u, token in zip(
            ["common_tags", "most_tagged"], [self.user_token, self.verif_user_token]
        ):
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
            response = self.client.get(reverse(u))
            self.assertEqual(
                response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data
            )
        # good case for admin role
        for u in ["common_tags", "most_tagged"]:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
            response = self.client.get(reverse(u))
            self.assertEqual(
                response.status_code, status.HTTP_200_OK, msg=response.data
            )
