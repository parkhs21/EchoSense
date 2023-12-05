# from langchain.chat_models import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
# from langchain.schema.output_parser import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough
# import dotenv
# dotenv.load_dotenv()


# prompt = ChatPromptTemplate.from_template(
#     "Tell me a short joke about {topic}"
# )
# output_parser = StrOutputParser()
# model = ChatOpenAI(model="gpt-3.5-turbo")
# chain = (
#     {"topic": RunnablePassthrough()} 
#     | prompt
#     | model
#     | output_parser
# )

# # print(chain.invoke("ice cream"))

# for chunk in chain.stream("ice cream"):
#     print(chunk, end="", flush=True)
# print()


from openai import OpenAI
import dotenv
dotenv.load_dotenv()

client = OpenAI()

audio = open("../recording.webm", "rb")
transcript = client.audio.transcriptions.create(
    file=audio,
    model="whisper-1", 
    language="ko",
    response_format="text"
)

print(transcript)

