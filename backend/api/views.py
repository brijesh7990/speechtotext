# views.py
import base64
import json
import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from django.conf import settings
from .models import AudioRecord
from .serializers import AudioRecordSerializer

# Bhashini API details
BHASHINI_API_URL = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
BHASHINI_API_KEY = "PcYD3f6WgosaSlLXLa7K7f5OteKLYQ6Cjyn0dyHEt2Fm7Ho7Sq-oo44N73XZvdDs"

class ProcessAudioView(APIView):
    """
    Handles uploading audio files and processing them with Bhashini API.
    """
    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({"error": "No file part in the request"}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        
        try:
            # Convert audio file to base64
            audio_base64 = base64.b64encode(file.read()).decode('utf-8')
            payload = {
                "pipelineTasks": [
                    {
                        "taskType": "asr",
                        "config": {
                            "language": {
                                "sourceLanguage": "gu"
                            },
                            "audioFormat": "wav",
                            "samplingRate": 16000
                        }
                    }
                ],
                "inputData": {
                    "audio": [
                        {
                            "audioContent": audio_base64
                        }
                    ]
                }
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {BHASHINI_API_KEY}",
            }

            # Send request to Bhashini API
            response = requests.post(BHASHINI_API_URL, headers=headers, data=json.dumps(payload))

            if response.status_code == 200:
                transcription = response.json().get('pipelineResponse', [{}])[0].get('output', [{}])[0].get('source', '')
                
                # Save the audio file and transcription to the database
                audio_record = AudioRecord.objects.create(
                    audio_file=file,
                    original_transcription=transcription
                )
                serializer = AudioRecordSerializer(audio_record)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "ASR service failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EditTranscriptionView(RetrieveUpdateAPIView):
    """
    Handles retrieving and updating the edited transcription of an audio record.
    """
    queryset = AudioRecord.objects.all()
    serializer_class = AudioRecordSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        edited_transcription = request.data.get('edited_transcription', None)
        if edited_transcription:
            instance.edited_transcription = edited_transcription
            instance.save()
            return Response(AudioRecordSerializer(instance).data, status=status.HTTP_200_OK)
        return Response({"error": "No edited transcription provided"}, status=status.HTTP_400_BAD_REQUEST)
