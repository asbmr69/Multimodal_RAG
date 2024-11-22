import os
import sys
import asyncio
from langchain_openai import ChatOpenAI
from browser_use import Agent, Controller

# Verify environment variable
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set!")

# Set up model and controller
controller = Controller()
model = ChatOpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key= api_key,

    model='gpt-4o',
	
)

# Initialize agents
agent1 = Agent(
    task='Open 2 tabs with Wikipedia articles about the history of Meta and one random Wikipedia article.',
    llm=model,
    controller=controller,
)
agent2 = Agent(
    task='Considering all open tabs, give me the names of the Wikipedia articles.',
    llm=model,
    controller=controller,
)

async def main():
    await agent1.run()
    await agent2.run()

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
