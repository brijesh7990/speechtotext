import requests
url = "https://bhashini.gov.in/api/pipeline/compute"

headers = {
    "Authorization": "Bearer 2865f6f153-8402-4aba-8442-b928ecfaa612",
    "Content-Type": "application/json"
}

data = {
    "pipelineId": "YOUR_PIPELINE_ID",
    "input": {
        "audio": "path_to_your_audio_file",
        "sourceLanguage": "en",  # Assuming the audio is in English
        "targetLanguage": "gu"
    }
}

# Send the request
response = requests.post(url, json=data, headers=headers)

# Handle the response
if response.status_code == 200:
    print("Translated text:", response.json()["output"]["translation"])
else:
    print("Error:", response.status_code, response.text)