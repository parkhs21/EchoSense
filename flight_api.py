import os

os.environ["AMADEUS_CLIENT_ID"] = "xxx"
os.environ["AMADEUS_CLIENT_SECRET"] = "xxx"
os.environ["OPENAI_API_KEY"] = "sk-xxx"

from langchain.agents.agent_toolkits.amadeus.toolkit import AmadeusToolkit

toolkit = AmadeusToolkit()
tools = toolkit.get_tools()

from langchain.agents import AgentType, initialize_agent
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    verbose=False,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
)

print(agent.run(
    "2023년 12월에 출발하는 서울에서 미국으로 가는 비행기 중 가장 저렴한 티켓의 가격과 출발 시간을 알려줘"
))