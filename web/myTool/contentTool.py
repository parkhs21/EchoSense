import numpy as np
import cv2
import os
import uuid
import soundfile as sf

CACHE_DIRECTORY = "./cache"

def preprocess_image(image: np.ndarray) -> np.ndarray:
    image = np.fliplr(image)
    return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

def cache_image(image: np.ndarray) -> str:
    image_filename = f"{uuid.uuid4()}.jpeg"
    os.makedirs(CACHE_DIRECTORY, exist_ok=True)
    image_path = os.path.join(CACHE_DIRECTORY, image_filename)
    cv2.imwrite(image_path, image)
    return image_path

def cache_audio(audio: (int, np.ndarray)) -> str:
    audio_filename = f"{uuid.uuid4()}.wav"
    os.makedirs(CACHE_DIRECTORY, exist_ok=True)
    audio_path = os.path.join(CACHE_DIRECTORY, audio_filename)
    sf.write(audio_path, audio[1], audio[0])
    return audio_path