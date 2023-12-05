from langchain.retrievers.web_research import WebResearchRetriever
import os
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models.openai import ChatOpenAI
from langchain.utilities import GoogleSearchAPIWrapper

os.environ["OPENAI_API_KEY"] = "sk-xxx"
os.environ["GOOGLE_CSE_ID"] = "xxx"
os.environ["GOOGLE_API_KEY"] = "xxx-xxx"

vector_store = Chroma(embedding_function=OpenAIEmbeddings(),
                      persist_directory="./chroma_db_oai")

search_llm = ChatOpenAI(temperature=0) # Search Query를 위한 LLM

search = GoogleSearchAPIWrapper() # SearchAPI Wrapper 객체 생성

# Web Research Retriever
web_research_retriever = WebResearchRetriever.from_llm(
    llm=search_llm,
    vectorstore=vector_store,
    search=search,
)

from langchain.chains import RetrievalQAWithSourcesChain
response_llm = ChatOpenAI(temperature=0.9)
qa_chain = RetrievalQAWithSourcesChain.from_chain_type(response_llm, 
                                                       retriever = web_research_retriever)

user_input = "When is Newzine's Minji's birthday??"
result = qa_chain({"question": user_input})
print(result)