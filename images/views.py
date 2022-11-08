from rest_framework.generics import ListAPIView

from .models import Image
from .serializers import ImageSerializer


class ImageView(ListAPIView):
    queryset = Image.objects.order_by("-created_at")
    serializer_class = ImageSerializer
