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
