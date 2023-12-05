from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000/"], # 클라이언트 도메인에 대해 CORS 허용
    allow_credentials=True,
    allow_methods=["*"], # 모든 HTTP 메소드에 대해 CORS 허용
    allow_headers=["*"], # 모든 HTTP 헤더에 대해 CORS 허용
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/upload")
async def upload_file(content: UploadFile = File(...), location: str = Form(...)):
    file_path = f"./{content.filename}"
    with open(file_path, "wb") as file:
        file.write(content.file.read())

    location_data = json.loads(location)
    
    # 추가적인 로직

    return {"message": "파일이 성공적으로 업로드되었습니다.",
            "filename": content.filename,
            "location": location_data
            }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)