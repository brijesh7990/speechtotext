from django.urls import path
from .views import TranscriptionView

urlpatterns = [
    # path('transcribe/', TranscriptionView.as_view(), name='audio-transcription')
    path('process_audio/', ProcessAudioView.as_view(), name='process_audio'),
    path('edit_transcription/<int:pk>/', EditTranscriptionView.as_view(), name='edit_transcription'),
]
