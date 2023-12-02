import React, { useState, useRef } from 'react';
import axios from 'axios';

const RecordButton = () => {
  const [recording, setRecording] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null);
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
      const audioUrl = URL.createObjectURL(audioBlob);
      setAudioUrl(audioUrl);
    }
  };

  return (
    <div>
      <button onClick={recording ? stopRecording : startRecording}>
        {recording ? '녹음 중지' : '녹음 시작'}
      </button>
      {audioUrl && <a href={audioUrl} download="recording.wav">다운로드</a>}
    </div>
  );
};

export default RecordButton;