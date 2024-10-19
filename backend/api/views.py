# api/views.py
import base64
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AudioUploadSerializer

class TranscriptionView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AudioUploadSerializer(data=request.data)
        if serializer.is_valid():
            audio_file = serializer.validated_data['audio']

            # Convert the audio file to base64
            audio_content = audio_file.read()
            base64_audio = base64.b64encode(audio_content).decode('utf-8')

            # Create payload for Bhashini API
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
                            "audioContent": base64_audio
                        }
                    ]
                }
            }

            # Make a POST request to the Bhashini API
            try:
                response = requests.post(
                    'https://dhruva-api.bhashini.gov.in/services/inference/pipeline',
                    json=payload,
                    headers={
                        'Authorization': 'PcYD3f6WgosaSlLXLa7K7f5OteKLYQ6Cjyn0dyHEt2Fm7Ho7Sq-oo44N73XZvdDs',
                        'Content-Type': 'application/json',
                    },
                )
                response_data = response.json()
                print("response_data", response_data.get("pipelineResponse")[0].get("output")[0].get("source"))
                transcription = response_data.get('transcription', response_data.get("pipelineResponse")[0].get("output")[0].get("source"))

                return Response({'transcription': transcription}, status=status.HTTP_200_OK)
            except requests.exceptions.RequestException as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
