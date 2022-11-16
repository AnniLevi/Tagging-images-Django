import os
import uuid

from django.contrib.auth.models import User
from django.db import models

from utils.validators import validate_image_format, validate_image_size


class Image(models.Model):
    name = models.CharField(max_length=200)
    img = models.ImageField(
        upload_to="images/", validators=[validate_image_size, validate_image_format]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return self.name

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.img.name = self.create_image_name(self.img.name)
        return super().save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )

    @staticmethod
    def create_image_name(image_name: str) -> str:
        """Creates a random image name, keeping the extension."""
        img_extension: str = os.path.splitext(image_name)[1]
        return "{}{}".format(uuid.uuid4().hex[:30], img_extension)


class Tag(models.Model):
    tag = models.CharField(max_length=100)
    img = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="tags")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tags")
    created_at = models.DateTimeField(auto_now_add=True)
