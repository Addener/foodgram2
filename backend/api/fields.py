import base64

from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageFieldSerializer(serializers.ImageField):
    """Сериализатор для обработки полей изображений."""

    def to_internal_value(self, data):
        """Обработка изображений."""
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)