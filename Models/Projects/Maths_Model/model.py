# For UI
import streamlit as st 

# LLM / Models 
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Prompt
from langchain_core.prompts import PromptTemplate

#chains
from langchain_classic.chains.llm_math.base import LLMMathChain
from langchain_classic.chains.llm import LLMChain
from langchain_community.utilities import WikipediaAPIWrapper

from langchain_classic.agents.agent_types import AgentType
# from langchain_core.tools import Tool
from langchain_classic.agents import initialize_agent,Tool
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
import re

load_dotenv()


st.title("Maths Problem solver Chat Bot")

sidebar = st.sidebar

sidebar.title("Settings")
grok_apikey = sidebar.text_input("Enter your GROQ API KEY",type="password")
if not grok_apikey:
    st.info("Please enter the api key")
    st.stop()

model = ChatGroq(model='llama-3.1-8b-instant',api_key=grok_apikey)

wikipedia = WikipediaAPIWrapper()
wiki_tool = Tool(
    func=wikipedia.run,name="Wiki Tool",description="Agent used for searching over the internet to find various information"
)

def math_tool(question):
    math = ''.join()
