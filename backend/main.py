from flask import Flask, request, jsonify
import requests
import json
import base64

# Initialize Flask app
app = Flask(__name__)

# Define the URL for the external API
url = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"

# Define headers for the external API
headers = {
    "Content-Type": "application/json",
    # "User-Agent": "PostmanRuntime/7.42.0",
    # "Accept": "*/*",
    # "Accept-Encoding": "gzip, deflate, br",
    # "Connection": "keep-alive",
    "Authorization": "PcYD3f6WgosaSlLXLa7K7f5OteKLYQ6Cjyn0dyHEt2Fm7Ho7Sq-oo44N73XZvdDs"
}

# Define the API route that accepts an audio file
@app.route('/process_audio', methods=['POST'])
def process_audio():
    # Check if the 'file' key exists in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    # Ensure the file is provided
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Read the audio file and encode it to base64
        audio_base64 = base64.b64encode(file.read()).decode('utf-8')

        # Prepare the payload
        payload = {
            "pipelineTasks": [
                {
                    "taskType": "asr",
                    "config": {
                        "language": {
                            "sourceLanguage": "gu"  # Assuming Gujarati
                        },
                        "serviceId": "",
                        "audioFormat": "flac",
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

        # Make a POST request to the external API
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # Check if the request to the external API was successful
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": "Failed to process audio"}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)