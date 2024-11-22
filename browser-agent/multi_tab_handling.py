"""
Simple try of the agent.

@dev You need to add OPENAI_API_KEY to your environment variables.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from langchain_openai import ChatOpenAI

from browser_use import Agent

llm = ChatOpenAI(model='gpt-4o')
agent = Agent(
	task='open 3 tabs with prime minister of india, prime minister of usa, and prime minister of japan, then go back to the first and click on the first link',


	llm=llm,
)


async def main():
	await agent.run()


asyncio.run(main())