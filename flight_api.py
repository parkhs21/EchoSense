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

agent.run("What is the departure time of the cheapest flight on August 23, 2023 leaving Dallas, Texas before noon to Lincoln, Nebraska?")