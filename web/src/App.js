import React, { useState, useRef, useEffect, useCallback } from 'react';
import axios from 'axios';
import './App.css'

const Main = () => {
  const [recording, setRecording] = useState(false);
  const [capturing, setCapturing] = useState(false);
  const mediaRecorderRef = useRef(null);
  const videoRef = useRef(null);
  
  const startRecording = () => { setRecording(true); }
  const startCapturing = () => { setCapturing(true); }

  const getLocation = async() => {
    return new Promise((resolve, reject) => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
          resolve({
            'latitude': position.coords.latitude,
            'longitude': position.coords.longitude
          });
        });
      } else {
        console.error('브라우저가 위치정보 사용을 지원하지 않습니다.');
        reject('브라우저가 위치정보 사용을 지원하지 않습니다.');
      }
    });
  };
  
  const stopping = () => {
    mediaRecorderRef.current.stop();
    mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
  };

  const handleDataAvailable = useCallback(async (event) => {
    if (event.data.size > 0) {
      const dataBlob = new Blob([event.data], {
        type: capturing ? 'video/webm' : 'audio/webm'
      });
      
      setRecording(false);
      setCapturing(false);

      const location = await getLocation();
      if (!location) throw new Error('위치정보를 가져올 수 없습니다.');
  
      const formData = new FormData();
      formData.append('content', dataBlob, 'recording.webm');
      formData.append('location', JSON.stringify(location));

      try {
        const response = await axios.post('http://localhost:8000/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        console.log('파일이 성공적으로 전송되었습니다:', response);
      } catch (error) {
        console.error('오류 발생:', error);
      }
    };

  }, [capturing]);

  const starting = useCallback(async () => {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
        video: capturing
      });

      if (capturing) videoRef.current.srcObject = stream;

      mediaRecorderRef.current = new MediaRecorder(stream, {
        mimeType: capturing ? 'video/webm' : 'audio/webm'
      });
      mediaRecorderRef.current.ondataavailable = handleDataAvailable;

      mediaRecorderRef.current.start();
    } else {
      console.error('브라우저가 해당 미디어를 지원하지 않습니다.');
    }
  }, [capturing, handleDataAvailable]);

  useEffect(() => {
    if (capturing || recording) {
      starting();
    }
  }, [capturing, recording]);

  return (
    <div className='container'>
      <span className='title'>EchoSense</span>
      {
        capturing ?
          <video className='webcam' ref={videoRef} autoPlay playsInline muted/>
          :
          <div className='emptyBox'></div>
      }
      <div>
        <button className='btn' onClick={recording ? stopping : startRecording} disabled={capturing}>
            {recording ? '녹음 중지' : '녹음 시작'}
        </button>
        <button className='btn' onClick={capturing ? stopping : startCapturing} disabled={recording}>
            {capturing ? '녹화 중지' : '녹화 시작'}
        </button>
      </div>
    </div>
  );
};

export default Main;