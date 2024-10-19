from django.urls import path
from .views import AudioTranscriptionView

urlpatterns = [
    path('transcribe/', AudioTranscriptionView.as_view(), name='audio-transcription')
]
