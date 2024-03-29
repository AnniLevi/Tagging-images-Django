import io
import typing
import zipfile

from django.core.files.images import ImageFile
from rest_framework import serializers

from utils.validators import (
    validate_image_format,
    validate_image_size,
    validate_zip_archive_size,
)

from .models import Image, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "tag", "img_id", "user_id", "created_at")

    img_id = serializers.IntegerField()

    def create(self, validated_data: dict) -> Tag:
        user_id: int = self.context["request"].user.id
        validated_data["user_id"] = user_id
        return super().create(validated_data)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "name", "img", "user_id", "created_at", "tags")

    tags = TagSerializer(many=True, read_only=True)

    def create(self, validated_data: dict) -> Image:
        validated_data["user_id"] = self.context["request"].user.id
        return super().create(validated_data)


class ZipImageSerializer(serializers.Serializer):
    class Meta:
        fields = ("zip_archive",)

    zip_archive = serializers.FileField()

    def validate_zip_archive(self, obj: typing.IO[bytes]) -> typing.IO[bytes]:
        if not zipfile.is_zipfile(obj):
            raise serializers.ValidationError("zip archive is required")
        zp: zipfile.ZipFile = zipfile.ZipFile(obj)
        validate_zip_archive_size(zp)
        for filename in zp.namelist():
            file: bytes = zp.read(filename)
            img: ImageFile = ImageFile(io.BytesIO(file))
            validate_image_size(img)
            validate_image_format(img)
        return obj

    def create(self, validated_data: dict) -> dict:
        zp: zipfile.ZipFile = zipfile.ZipFile(validated_data["zip_archive"])
        objs: typing.List[Image] = []
        for filename in zp.namelist():
            objs.append(
                Image(
                    name=filename,
                    img=ImageFile(
                        io.BytesIO(zp.read(filename)),
                        name=Image.create_image_name(filename),
                    ),
                    user_id=self.context["user"].id,
                )
            )
        Image.objects.bulk_create(objs)
        return validated_data


class ImageCommonTagsSerializer(serializers.Serializer):
    class Meta:
        fields = ("id", "img_name", "tag", "tags_count")

    id = serializers.IntegerField()
    img_name = serializers.CharField(source="name")
    tag = serializers.CharField(source="tags__tag")
    tags_count = serializers.IntegerField()


class ImageFreqTaggedSerializer(serializers.Serializer):
    class Meta:
        fields = ("id", "img_name", "tags_count")

    id = serializers.IntegerField()
    img_name = serializers.CharField(source="name")
    tags_count = serializers.IntegerField()
