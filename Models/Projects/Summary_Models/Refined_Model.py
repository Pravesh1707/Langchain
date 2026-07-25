#Summary Chain
from langchain_classic.chains.summarize import load_summarize_chain

#Chat Model
from langchain_huggingface import ChatHuggingFace
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

from dotenv import load_dotenv

#Prompt
from langchain_core.prompts import PromptTemplate

# Document Loader
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

#UI 
import streamlit as st 

load_dotenv()

def load_data(file):
    temp_file = './temp_date'
    with open(temp_file,'wb') as f:
        f.write(file.getvalue())

    return temp_file

chunks=[]

st.title('Refine Summarize chain')

uploaded_file = st.file_uploader('Uplload File',type=['pdf'])
upload_btn = st.button('Process Document')

if upload_btn:
    file = load_data(uploaded_file)
    loader = PyPDFLoader(file)
    doc = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    data = splitter.split_documents(doc)

    model = ChatGroq(model='llama-3.1-8b-instant')

    initial_prompt = PromptTemplate(
        template='Write a concise summary of the following text:\n{text}',
        input_variables=['text']
    )
    final_prompt = PromptTemplate(
        template='Your current summary is: {existing_answer}. Now refine and improve it using the following new text: {text}. Provide an updated, improved summary that includes important details from both the old and new text.',
        input_variables=['existing_answer', 'text']
    )

    chain = load_summarize_chain(
        llm=model,
        chain_type='refine',
        question_prompt=initial_prompt,
        refine_prompt=final_prompt,
        verbose=True
    )

    response = chain.run(data)
    st.write(response) 