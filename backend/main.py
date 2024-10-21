from flask import Flask, request, jsonify
import requests
import json
import base64
from flask_cors import CORS
import sqlite3

# Initialize Flask app
app = Flask(__name__)

CORS(app)

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


@app.route('/hello', methods=['GET'])
def hello():
    return "hello"
# Define the API route that accepts an audio file

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    try:
        # Log the incoming file info

        # Read and encode the audio file to base64
        audio_base64 = base64.b64encode(file.read()).decode('utf-8')

        # Prepare the payload
        payload = {
            "pipelineTasks": [
                {
                    "taskType": "asr",
                    "config": {
                        "language": {
                            "sourceLanguage": "gu"
                        },
                        "serviceId": "",
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


        # Send request to the external API
        print('calling bhasini api ...')
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            try :
                source = response.json()['pipelineResponse'][0]['output'][0]['source']
                print(jsonify({"text":source}))
                conn = sqlite3.connect('audio_data.db')
                cursor = conn.cursor()
                cursor.execute('''
                        INSERT INTO audio_records (audio_base64, source) VALUES (?, ?)
                    ''', (audio_base64, source))
                new_id = cursor.lastrowid
                conn.commit()
                conn.close()
                return jsonify({"text":source, 'id':new_id}), 200
            except :
                return jsonify({"error": "audio proccessed, format error"}), response.status_code
        else:
            return jsonify({"error": "Failed to process audio"}), response.status_code

    except Exception as e:
        # Log the error for debugging
        return jsonify({"error": str(e)}), 500


@app.route('/submit_audio', methods=['POST'])
def submit_audio():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        if not data or not data.get('id') or not data.get('text'):
            # Return error response if required data is missing
            return jsonify({'status': 'fail', 'message': 'Missing id or text'}), 400

        # Extract data
        id = int(data['id'])
        text = data['text']

        print("brijesh id1 ===", id)
        print("brijesh text1 ===", text)

        # Connect to the SQLite database
        connection = sqlite3.connect('audio_data.db')
        cursor = connection.cursor()
        print("brijesh id ===", id)
        print("brijesh text ===", text)

        # Update the record in the database
        cursor.execute("""
            UPDATE audio_records
            SET edit_source = ?
            WHERE id = ?;
        """, (text, id))

        # Commit changes to the database
        connection.commit()

        # Check if any rows were affected (record updated)
        if cursor.rowcount == 0:
            return jsonify({'status': 'fail', 'message': 'Record not found'}), 404

        # Close the connection
        connection.close()

        # Return success response
        return jsonify({'status': 'success', 'message': 'Record updated successfully'}), 200

    except sqlite3.Error as e:
        # Handle database-related errors
        return jsonify({'status': 'fail', 'message': f'Database error: {str(e)}'}), 500

    except Exception as e:
        # Handle any other exceptions
        return jsonify({'status': 'fail', 'message': f'An error occurred: {str(e)}'}), 500


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)