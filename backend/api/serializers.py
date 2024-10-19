from rest_framework import serializers

class AudioUploadSerializer(serializers.Serializer):
    audio = serializers.FileField()
