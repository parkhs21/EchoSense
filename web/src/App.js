import React, { useState, useRef } from 'react';
import axios from 'axios';

const RecordButton = () => {
  const [recording, setRecording] = useState(false);
  const mediaRecorderRef = useRef(null);

  const startRecording = async () => {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      mediaRecorderRef.current = new MediaRecorder(stream, { mimeType: 'audio/webm' });
      mediaRecorderRef.current.ondataavailable = handleDataAvailable;

      mediaRecorderRef.current.start();
      setRecording(true);
    } else {
      console.error('브라우저가 오디오 녹음을 지원하지 않습니다.');
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
    setRecording(false);
  };

  const handleDataAvailable = async (event) => {
    if (event.data.size > 0) {
      const audioBlob = new Blob([event.data], { type: 'audio/wav' });
  
      const formData = new FormData();
      formData.append('audioFile', audioBlob, 'recording.wav');
  
      try {
        const response = await axios.post('http://localhost:8000/upload-audio', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
  
        console.log('오디오 파일이 성공적으로 전송되었습니다:', response);
      } catch (error) {
        console.error('오류 발생:', error);
      }
    }
  };

  return (
    <div>
      <button onClick={recording ? stopRecording : startRecording}>
        {recording ? '녹음 중지' : '녹음 시작'}
      </button>
    </div>
  );
};

export default RecordButton;