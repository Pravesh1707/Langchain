
# Models
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_huggingface import ChatHuggingFace

from dotenv import load_dotenv

#Prompt Template
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

#UI
import streamlit as st 

#Keys
load_dotenv()

#Models
model = ChatOpenAI(model='gpt-4o')
# model = ChatGroq(model='llama-3.1-8b-instnt')
# model = ChatHuggingFace(model='mistral')

#Prompt
prompt = PromptTemplate(template='You are an Expert text summarizer which helps summarizing text in {words} words. Help me summarize this textx : \n {text}',input_variables=['words','text'])

st.title('Text Summarizer')

text = st.text_input('Please enter text you need to Summarize')
words = st.text_input('Define number of words you want summary in. ( > 50)')
# final_prompt = prompt.format({'words':words,'text': text})


if st.button('Summarize'):
    chain = prompt | model

    response = chain.invoke({'words':words,'text': text})
    st.write(response.content)





