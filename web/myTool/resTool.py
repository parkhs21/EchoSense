import requests

ENDPOINT = "http://localhost:8000"

def prompt_stt(audio_path: str) -> str:
    detail = "/upload"
    files = {"content" : open(audio_path, "rb")}
    response = requests.post(ENDPOINT+detail, files=files).json()
    return response.get("transcript")

def prompt_chat(prompt: str) -> str:
    location = current_location()
    detail = "/prompt-chat/invoke"
    body = {"input": {"text": prompt}}
    response = requests.post(ENDPOINT+detail, json=body).json()
    return response.get("output")

def prompt_image(image_path: str, prompt: str) -> str:
    location = current_location()
    detail = "/upload-image"
    files = {"content" : open(image_path, "rb"), "prompt": (None, prompt)}
    response = requests.post(ENDPOINT+detail, files=files).json()
    return response.get("output").get("content")


def current_location() -> dict:
    here_req = requests.get("http://www.geoplugin.net/json.gp")

    if (here_req.status_code != 200):
        print("현재좌표를 불러올 수 없음")
    else:
        location = here_req.json()
        crd = {"lat": location.get("geoplugin_latitude"), "lng": location.get("geoplugin_longitude")}
    return crd
    