from langchain_classic.chains.summarize import load_summarize_chain

from langchain_huggingface import ChatHuggingFace
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import streamlit as st 

load_dotenv()

def load_data(file):
    temp_file = './temp_date'
    with open(temp_file,'wb') as f:
        f.write(file.getvalue())

    return temp_file

def store(file):
    loader = PyPDFLoader(file)
    doc = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    data = splitter.split_documents(doc)
    return data

chunks=[]

st.title('Map Reduced Summarize chain')

uploaded_file = st.file_uploader('Uplload File',type=['pdf'])
upload_btn = st.button('Process Document')

if upload_btn:
    file = load_data(uploaded_file)
    loader = PyPDFLoader(file)
    doc = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    data = splitter.split_documents(doc)

    model = ChatGroq(model='llama-3.1-8b-instant')

    initial_prompt = PromptTemplate(template='write a collictive summary of the given text: \n {text}',input_variables=['text'])
    # final_prompt = PromptTemplate(template='Write a Detailed Summary of the following text \n {text}',input_variables=['text'])

    chain = load_summarize_chain(llm=model,chain_type='map_reduce',map_prompt=initial_prompt,combine_prompt=initial_prompt,verbose=True)

    response = chain.run(data)
    st.write(response)