from zipfile import ZipFile

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile
from PIL import Image, UnidentifiedImageError


def validate_image_size(obj: ImageFile) -> None:
    filesize: int = obj.size
    if filesize > settings.IMAGE_MAX_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"Image max size is {settings.IMAGE_MAX_SIZE_MB}MB")


def validate_image_format(obj: ImageFile) -> None:
    try:
        im: Image = Image.open(obj.file)
        if im.format not in settings.IMAGE_FORMATS:
            raise ValidationError(f"Supported formats: {settings.IMAGE_FORMATS}")
    except UnidentifiedImageError as e:
        raise ValidationError(e.args[0])


def validate_zip_archive_size(obj: ZipFile) -> None:
    size: int = sum([item.file_size for item in obj.filelist])
    size_mb: float = size / 1024 / 1024
    if size_mb > settings.ZIP_MAX_SIZE_MB:
        raise ValidationError(f"Zip archive max size is {settings.ZIP_MAX_SIZE_MB}MB")
