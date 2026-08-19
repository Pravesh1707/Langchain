from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import ChatPromptTemplate
from ddgs import DDGS
# import wikipedia
from typing import List

from langchain_classic.tools import tool
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent

@tool
def web_search(query : str) -> str:
    """Use DuckDuckGo web search. Retuen up to 'max_results' ompact results with URLs and snippets."""

    try:
        with DDGS() as ddg:
            hits = list(ddg.text(query))
        return str(hits)
    except Exception as e:
        return f"Error. : {e}"


def search_agent():
    model = ChatOpenAI(model="gpt-4o")
    tool = [web_search]
    prompt = ChatPromptTemplate.from_messages([("system","You are an Professional News Ancor. Use Available tools to answer the user query correctly"),
                                               ("human","{input}")])

    tool_agent = create_tool_calling_agent(llm=model,tools=tool,prompt=prompt)
    return AgentExecutor(agent=tool_agent,tools=tool)

agent = search_agent()

query = input("Ask your query : ")
while not query == "exit":
    result = agent.invoke({"input":query})
    print(result["output"])
    query = input("Ask your next Query : ")