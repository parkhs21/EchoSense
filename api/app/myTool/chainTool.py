from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from app.myTool import contentTool, chainTool

def pp(prompt):
    print(prompt)
    return prompt
rpp = RunnableLambda(pp)

chat_prompt = ChatPromptTemplate.from_template("{text}")
output_parser = StrOutputParser()
chat_model = ChatOpenAI(model="gpt-3.5-turbo")
chat_chain = (
    chat_prompt
    | chat_model
    | output_parser
)

# def image_prompt(text, base64_image):
#     return 
# image_model = ChatOpenAI(model="gpt-4-vision-preview")
# image_chain = (
#     image_model
#     | output_parser
# )