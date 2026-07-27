# For UI
import streamlit as st 

# LLM / Models 
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Prompt
from langchain_core.prompts import PromptTemplate

load_dotenv()