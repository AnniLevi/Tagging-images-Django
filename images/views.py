from django.core.exceptions import PermissionDenied
from django.db.models import Count, Prefetch
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import check_user_group

from .models import Image, Tag
from .serializers import (
    ImageCommonTagsSerializer,
    ImageFreqTaggedSerializer,
    ImageSerializer,
    TagSerializer,
    ZipImageSerializer,
)


class ImageView(ListCreateAPIView):
    serializer_class = ImageSerializer

    @swagger_auto_schema(
        responses={status.HTTP_201_CREATED: ImageSerializer()},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "img": openapi.Schema(type=openapi.TYPE_FILE),
            },
        ),
    )
    def post(self, request, *args, **kwargs):
        if not check_user_group(self.request.user, [1, 2]):
            raise PermissionDenied
        return self.create(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ImageSerializer()},
        manual_parameters=[
            openapi.Parameter(
                "tagged",
                openapi.IN_QUERY,
                description="the available images that user have / have not yet tagged",
                type=openapi.TYPE_BOOLEAN,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):
        images_qs = Image.objects.order_by("-created_at")
        tags_qs = Tag.objects.order_by("-created_at")

        if not check_user_group(self.request.user, [1, 2]):
            tags_qs = tags_qs.filter(user=self.request.user)

        param = self.request.query_params.get("tagged")
        if param == "true":
            images_qs = images_qs.filter(tags__user=self.request.user).distinct()
        elif param == "false":
            images_qs = images_qs.exclude(tags__user=self.request.user)

        return images_qs.prefetch_related(Prefetch("tags", tags_qs))


class ZipImageView(APIView):
    queryset = Image.objects.order_by("-created_at")
    serializer_class = ZipImageSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "zip_archive": openapi.Schema(type=openapi.TYPE_FILE),
            },
        ),
    )
    def post(self, request, *args, **kwargs):
        if not check_user_group(self.request.user, [1, 2]):
            raise PermissionDenied
        serializer = ZipImageSerializer(
            data=request.data, context={"user": self.request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"ok": True}, status=status.HTTP_201_CREATED)


class TagView(ListCreateAPIView):
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user).order_by("-created_at")


class ImageCommonTagsView(ListAPIView):
    serializer_class = ImageCommonTagsSerializer

    def get_queryset(self):
        qs = (
            Image.objects.prefetch_related("tags")
            .values("id", "name", "tags__tag")
            .annotate(tags_count=Count("tags"))
            .order_by("-tags_count")
        )
        return qs

    def get(self, request, *args, **kwargs):
        if not check_user_group(self.request.user, [2]):
            raise PermissionDenied
        return self.list(request, *args, **kwargs)


class ImageFreqTaggedView(ListAPIView):
    serializer_class = ImageFreqTaggedSerializer

    def get_queryset(self):
        qs = (
            Image.objects.prefetch_related("tags")
            .values("id", "name")
            .annotate(tags_count=Count("tags"))
            .order_by("-tags_count")
        )
        return qs

    def get(self, request, *args, **kwargs):
        if not check_user_group(self.request.user, [2]):
            raise PermissionDenied
        return self.list(request, *args, **kwargs)
