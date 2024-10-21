from django.db import models

# Create your models here.

class AudioRecord(models.Model):
    audio_file = models.FileField(upload_to='media/audio_files/')
    original_transcription = models.TextField(blank=True, null=True)
    edited_transcription = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"AudioRecord {self.id}"