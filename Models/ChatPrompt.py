from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st 

load_dotenv()

role = st.text_input('Enter Role ')
query = st.text_area('Please type in your Query')

template = ChatPromptTemplate.from_messages([("system",'''You are a Senior {role} with 1+ decade of experiance'''),("human",'Help me understand {query} in 50 Words.')])

prompt = template.invoke({'role':role,'query':query})

model = ChatOpenAI(model='gpt-3.5-turbo')

response = model.invoke(prompt)

if st.button('Answer'):
    st.write(response.content)