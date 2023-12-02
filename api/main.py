from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/upload-audio")
async def upload_audio(audioFile: UploadFile = File(...)):
    file_location = f"uploads/{audioFile.filename}"
    with open(file_location, "wb") as file:
        file.write(audioFile.file.read())
    
    # 추가적인 로직

    return {"message": "오디오 파일이 성공적으로 업로드되었습니다.", "filename": audioFile.filename}