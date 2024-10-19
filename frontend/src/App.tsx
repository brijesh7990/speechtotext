import { useState, useRef } from 'react';
import axios from 'axios';
import { BsFillMicFill, BsFillStopFill } from 'react-icons/bs';
import { Button } from './components/ui/button';

const AudioRecorder: React.FC = () => {
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [recordings, setRecordings] = useState<string[]>([]);
  const [transcription, setTranscription] = useState<string | null>(null);
  const mediaRecorder = useRef<MediaRecorder | null>(null);
  const audioChunks = useRef<Blob[]>([]);

  const startRecording = async () => {
    try {
      setIsRecording(true);
      audioChunks.current = [];

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder.current = new MediaRecorder(stream);

      mediaRecorder.current.ondataavailable = (event: BlobEvent) => {
        audioChunks.current.push(event.data);
      };

      mediaRecorder.current.onstop = async () => {
        const audioBlob = new Blob(audioChunks.current, { type: 'audio/wav' });
        const url = URL.createObjectURL(audioBlob);
        setAudioUrl(url);
        setRecordings((prev) => [...prev, url]);

        // Send the audio to the Bhashini API for transcription
        await sendAudioToBhashini(audioBlob);
      };

      mediaRecorder.current.start();
    } catch (error) {
      console.error('Error starting audio recording:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder.current) {
      mediaRecorder.current.stop();
      setIsRecording(false);
    }
  };

  const sendAudioToBhashini = async (audioBlob: Blob) => {
    try {
      // Prepare the form data for sending the audio file
      const formData = new FormData();
      formData.append('audio', audioBlob, 'audio.wav');

      // Make a POST request to the Bhashini API
      const response = await axios.post('YOUR_API_ENDPOINT', formData, {
        headers: {
          'Authorization': `Bearer YOUR_API_KEY`,
          'Content-Type': 'multipart/form-data',
        },
      });

      // Assuming the API returns the transcription in Gujarati in a `transcription` field
      const gujaratiText = response.data.transcription;
      setTranscription(gujaratiText);
    } catch (error) {
      console.error('Error sending audio to Bhashini API:', error);
    }
  };

  return (
    <div className="flex flex-col items-center p-6 bg-white shadow-lg rounded-lg max-w-md mx-auto">
      <h2 className="text-2xl font-semibold mb-4">Audio Recorder</h2>
      <div className="flex justify-center items-center mb-4">
        {isRecording ? (
          <Button className="bg-red-500 text-white flex items-center" onClick={stopRecording}>
            <BsFillStopFill className="mr-2" /> Stop Recording
          </Button>
        ) : (
          <Button className="bg-green-500 text-white flex items-center" onClick={startRecording}>
            <BsFillMicFill className="mr-2" /> Start Recording
          </Button>
        )}
      </div>
      {audioUrl && (
        <audio controls className="w-full mb-4">
          <source src={audioUrl} type="audio/wav" />
          Your browser does not support the audio element.
        </audio>
      )}
      <div className="w-full">
        <h3 className="text-lg font-medium mb-2">Recordings:</h3>
        {recordings.length > 0 ? (
          <ul className="space-y-2">
            {recordings.map((url, index) => (
              <li key={index} className="flex items-center space-x-2">
                <audio controls className="w-full">
                  <source src={url} type="audio/wav" />
                </audio>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-500">No recordings yet.</p>
        )}
      </div>
      {transcription && (
        <div className="w-full mt-4">
          <h3 className="text-lg font-medium mb-2">Gujarati Transcription:</h3>
          <p className="bg-gray-100 p-4 rounded">{transcription}</p>
        </div>
      )}
    </div>
  );
};

export default AudioRecorder;
