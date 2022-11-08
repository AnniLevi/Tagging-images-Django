from django.core.exceptions import ValidationError
from PIL import Image


def validate_image_size(obj):
    limit_mb = 5
    filesize = obj.file.size
    if filesize > limit_mb * 1024 * 1024:
        raise ValidationError(f"Max file size is {limit_mb}MB")


def validate_image_format(obj):
    im = Image.open(obj.file)
    if im.format not in ("PNG", "JPEG"):
        raise ValidationError("Supported formats: png or jpeg")
