from rest_framework import serializers

class AudioUploadSerializer(serializers.Serializer):
    audio = serializers.FileField()

    def validate_audio(self, value):
        if not value.name.endswith(('.wav', '.mp3', '.webm')):
            raise serializers.ValidationError('Only .wav, .mp3, or .webm files are allowed.')
        return value