from rest_framework import serializers
from .models import AudioRecord

class AudioRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioRecord
        fields = ['id', 'audio_file', 'original_transcription', 'edited_transcription', 'created_at', 'updated_at']