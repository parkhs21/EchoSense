from app.myTool import contentTool, chainTool

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes

import dotenv
dotenv.load_dotenv()

app = FastAPI(
    title="EchoSense LangChain Serve",
    version="1.0",
    description="EchoSense LangChain Serve API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 클라이언트 도메인에 대해 CORS 허용
    allow_credentials=True,
    allow_methods=["*"], # 모든 HTTP 메소드에 대해 CORS 허용
    allow_headers=["*"], # 모든 HTTP 헤더에 대해 CORS 허용
)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

@app.post("/upload")
async def upload_file(content: UploadFile = File(...)):
    file_path = contentTool.cache_file(content)
    transcript = contentTool.prompt_stt(file_path)
    return {"transcript": transcript}

@app.post("/upload-image")
async def upload_file(content: UploadFile = File(...), prompt: str = Form(...)):
    file_path = contentTool.cache_file(content)
    response = contentTool.prompt_image(file_path, prompt)
    return {"output": response}


add_routes(app, chainTool.chat_chain, path="/prompt-chat")
# add_routes(app, chainTool.image_chain, path="/prompt-image")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
