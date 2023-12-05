from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
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

model = ChatOpenAI()
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
add_routes(
    app,
    prompt | model,
    path="/joke",
)

add_routes(
    app,
    ChatOpenAI(),
    path="/chat",
)


model_vision = ChatOpenAI(model="gpt-3.5-vision")
add_routes(
    app,
    model_vision,
    path="/echosense",
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
