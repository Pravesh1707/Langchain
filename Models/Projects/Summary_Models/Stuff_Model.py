
# Models
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_huggingface import ChatHuggingFace
from dotenv import load_dotenv

#Chain
from langchain_classic.chains.summarize import load_summarize_chain
#Doc_Loader
from langchain_community.document_loaders import PyPDFLoader

#Prompt Template
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

#UI
import streamlit as st 

#Keys
load_dotenv()

def Get_file(file):
    temp_file = './temp.pdf'
    with open(temp_file,'wb') as f:
        f.write(file.getvalue())
    return temp_file

#Models
model = ChatOpenAI(model='gpt-4o')
# model = ChatGroq(model='llama-3.1-8b-instnt')
# model = ChatHuggingFace(model='mistral')

#Prompt
prompt = PromptTemplate(template='You are an Expert text summarizer. Help me summarize this text : \n {text}',input_variables=['text'])

st.title('Stuff Text Summarizer')

file = st.file_uploader('Upload_file',type='pdf')
if file:
    doc = Get_file(file)

    loader = PyPDFLoader(doc)
    load_split = loader.load_and_split()

    if st.button('Summarize'):
        chain = load_summarize_chain(llm=model,chain_type='stuff',verbose=True,prompt=prompt)

        response = chain.run(load_split)
        st.write(response)