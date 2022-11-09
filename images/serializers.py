from rest_framework import serializers

from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "name", "img", "created_at", "user_id")

    user_id = serializers.SerializerMethodField()

    def get_user_id(self, obj):
        return obj.user.id

    def create(self, validated_data):
        user_id = self.context["request"].user.id
        validated_data["user_id"] = user_id
        return super().create(validated_data)
