from dotenv import load_dotenv
import streamlit as st 
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI


context = st.text_area('Select Role')
query = st.text_area('Please type in your query')
message = [SystemMessage(content='You are a Senior {context} with 10+ years of experience of working in an IT Company use your experience to answer the question.'),
           HumanMessage(content=query)]


model = ChatOpenAI(model='gpt-40')
response = model.invoke(message)

print(AIMessage(content=response.content))