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
        const audioBlob = new Blob(audioChunks.current, { type: 'audio/webm' });
        const wavBlob = await convertWebmToWav(audioBlob);
        const url = URL.createObjectURL(wavBlob);
        setAudioUrl(url);
        setRecordings((prev) => [...prev, url]);

        // Send the audio to the Bhashini API for transcription
        await sendAudioToBhashini(wavBlob);
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

  const convertWebmToWav = async (webmBlob: Blob): Promise<Blob> => {
    const audioContext = new AudioContext();
    const arrayBuffer = await webmBlob.arrayBuffer();
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
    const wavBuffer = audioBufferToWav(audioBuffer);
    return new Blob([wavBuffer], { type: 'audio/wav' });
  };

  const audioBufferToWav = (buffer: AudioBuffer): ArrayBuffer => {
    const numberOfChannels = buffer.numberOfChannels;
    const sampleRate = buffer.sampleRate;
    const format = 1; // 1 for PCM (uncompressed)
    const bitDepth = 16;

    const wavData = new DataView(new ArrayBuffer(44 + buffer.length * 2));
    let offset = 0;

    // Write WAV header
    writeString(wavData, offset, 'RIFF'); offset += 4;
    wavData.setUint32(offset, 36 + buffer.length * 2, true); offset += 4;
    writeString(wavData, offset, 'WAVE'); offset += 4;
    writeString(wavData, offset, 'fmt '); offset += 4;
    wavData.setUint32(offset, 16, true); offset += 4; // Subchunk1Size
    wavData.setUint16(offset, format, true); offset += 2; // AudioFormat
    wavData.setUint16(offset, numberOfChannels, true); offset += 2;
    wavData.setUint32(offset, sampleRate, true); offset += 4;
    wavData.setUint32(offset, sampleRate * numberOfChannels * (bitDepth / 8), true); offset += 4; // ByteRate
    wavData.setUint16(offset, numberOfChannels * (bitDepth / 8), true); offset += 2; // BlockAlign
    wavData.setUint16(offset, bitDepth, true); offset += 2;
    writeString(wavData, offset, 'data'); offset += 4;
    wavData.setUint32(offset, buffer.length * 2, true); offset += 4; // Subchunk2Size

    // Write PCM data
    const channelData = buffer.getChannelData(0);
    let i = 0;
    while (i < channelData.length) {
      wavData.setInt16(offset, channelData[i++] * 0x7FFF, true);
      offset += 2;
    }

    return wavData.buffer;
  };

  const writeString = (view: DataView, offset: number, str: string) => {
    for (let i = 0; i < str.length; i++) {
      view.setUint8(offset + i, str.charCodeAt(i));
    }
  };

  // Function to convert Blob to Base64
  const blobToBase64 = (blob: Blob): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(blob);
      reader.onloadend = () => {
        const base64String = reader.result?.toString().split(',')[1]; // Remove "data:*/*;base64,"
        resolve(base64String || '');
      };
      reader.onerror = () => {
        reject('Error reading blob as base64');
      };
    });
  };

  const sendAudioToBhashini = async (audioBlob: Blob) => {
    try {
      const base64Audio = await blobToBase64(audioBlob);
      const payload = {
        pipelineTasks: [
          {
            taskType: "asr",
            config: {
              language: {
                sourceLanguage: "gu"
              },
              serviceId: "",
              audioFormat: "wav",
              samplingRate: 16000
            }
          }
        ],
        inputData: {
          audio: [
            {
              audioContent: base64Audio
            }
          ]
        }
      };

      // Make a POST request to the Bhashini API
      const response = await axios.post('https://dhruva-api.bhashini.gov.in/services/inference/pipeline', payload, {
        headers: {
          'Authorization': `PcYD3f6WgosaSlLXLa7K7f5OteKLYQ6Cjyn0dyHEt2Fm7Ho7Sq-oo44N73XZvdDs`,
          'Content-Type': 'application/json',
        },
      });

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
