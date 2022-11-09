from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView

from .models import Image
from .serializers import ImageSerializer


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
