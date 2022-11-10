from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Image, Tag
from .serializers import ImageSerializer, TagSerializer, ZipImageSerializer


class ImageView(ListCreateAPIView):
    queryset = Image.objects.order_by("-created_at")
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
        return self.create(request, *args, **kwargs)


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
