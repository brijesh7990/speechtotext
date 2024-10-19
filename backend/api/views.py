import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AudioUploadSerializer
from django.conf import settings
from rest_framework.parsers import MultiPartParser
import json

class AudioTranscriptionView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = AudioUploadSerializer(data=request.data)
        if serializer.is_valid():
            audio_file = serializer.validated_data['audio']

            # Define the Bhasini API endpoint and your credentials
            url = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
            headers = {
                "Authorization": f"Bearer {settings.BHASINI_API_KEY}",
            }

            # Prepare the payload and files for the request
            files = {'audio': audio_file}
            data = {
                "pipelineId": "64392f96daac500b55c543cd",  # MeitY pipeline ID for ASR+NMT
                "input": {
                    "sourceLanguage": "en",  # Assuming the audio is in English
                    "targetLanguage": "gu"   # The desired output language (Gujarati)
                }
            }

            try:
                # Send the request to Bhasini
                response = requests.post(url, data={'json': json.dumps(data)}, files=files, headers=headers)
                print("brijesh-response-outside", dir(response))
                # print("brijesh-response-outside", response.json())

                
                # Log the response for debugging
                print("Response content:", response.content)
                print("Response status code:", response.status_code)

                # Check if the response is JSON
                if 'application/json' in response.headers.get('Content-Type', ''):
                    response_data = response.json()
                    print("brijesh response====", response)
                    if response.status_code == 200:
                        transcription = response_data.get("output", {}).get("translation", "No translation found")
                        return Response({"transcription": transcription}, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            "error": response_data.get("message", "An error occurred while processing the request.")
                        }, status=response.status_code)
                else:
                    return Response({
                        "error-in-else": f"Unexpected response format: {response.content.decode('utf-8')}"
                    }, status=response.status_code)

            except requests.exceptions.RequestException as e:
                return Response({"error": f"Request failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except ValueError:
                return Response({
                    "error": "Invalid response format from Bhasini API."
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
