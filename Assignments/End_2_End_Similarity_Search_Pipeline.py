
# Task 10 : End to End Similarity Search Pipeline

#Document Loaders
from langchain_community.document_loaders import TextLoader,PyMuPDFLoader,CSVLoader,WebBaseLoader

# Text Splitter for chunking
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Embedding Models
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

# Vector Stores
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS

from pathlib import Path
# Stramlit for UI
import streamlit as st 


def file_type(uploaded_file):
    return Path(uploaded_file).suffix.lower()

def pdf_loader(uploaded_file):
    loader = PyMuPDFLoader(uploaded_file)
    return loader.load()
def txt_loader(uploaded_file):
    loader = TextLoader(uploaded_file,encoding='utf-8')
    return loader.load()

def csv_loader(uploaded_file):
    loader = CSVLoader(uploaded_file,encoding='utf-8')
    return loader.load()

def Web_Loader(url):
    loader = WebBaseLoader(url)
    return loader.load()

def Text_Splitter(data):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    chunks = splitter.split_documents(data)
    return chunks

def Generate_embeddings(data,model,store):

    text = [chunk.page_content for chunk in data]

    if model == 'OpenAI':
        embedding = OpenAIEmbeddings(model="text-embedding-3-small")
        vector_store = store.from_documents(data,embedding)
        st.sidebar.success('Embedings Created Stat Searching')
        return vector_store

    elif model == 'Google Gemini':
        embedding = GoogleGenerativeAIEmbeddings(model='gimini-3.1-flash')
        vector_store = store.from_documents(data,embedding)
        st.sidebar.success('Embedings Created Stat Searching')
        return vector_store

    elif model == 'HuggingFace':
        embedding = HuggingFaceEmbeddings(model='sentence-transformers/all-mpnet-base-v2')
        vector_store = store.from_documents(data,embedding)
        st.sidebar.success('Embedings Created Stat Searching')
        return vector_store

    else:
        st.sidebar.write('select Embedding Model')
    return ""

def Web(url):
    loader = Web_Loader(url)
    # st.write(loader)
    st.sidebar.success(f'Document Loaded ')

    data = Text_Splitter(loader)
    # st.write(f'Chunk Length : {len(data)} \n {data}')

    st.sidebar.success(f'Chunks Size : {len(data)} ')

    return data


st.title('Mini Project - End to End Similarity Search Pipeline')

radio_opt = st.sidebar.radio('Where you want to search ?',options=['Web','File'])

if radio_opt == 'Web':
    url = st.sidebar.text_input('Provide the public URL ')
    loader_btn = st.sidebar.button('Start Process')

    if url and loader_btn:
        data = Web(url)
        
        embeding_model = st.sidebar.radio('Select Embedding Model',options=['OpenAI','Google Gemini','HuggingFace'])
        st.write(f'Selected Embeding Model : {embeding_model}')

        store = st.sidebar.radio('Select Vector Store',options=['FAISS','Chroma','InMemoryVectorStore'])
        st.write(f' Selected vector Store : {store}')

        embd_btn = st.sidebar.button('Embeding Doc')
        if embd_btn:
            vector_store = Generate_embeddings(data,embeding_model,store)
            st.sidebar.success('Vector Store Created')

            query = st.text_input('Ask Your Query from Document')
            try:
                response = vector_store.similarity_search(query)
                st.write(response)
            except Exception as e:
                st.write(f'Error : {e}')

else:
    uploaded_file = st.sidebar.file_uploader('Upload your file',type=['pdf','txt','csv'])
    if uploaded_file:
        file = file_type(uploaded_file.name)
        st.sidebar.write(f'file type : {file}')

        if file == '.pdf':
            loader = pdf_loader(uploaded_file.name)
        elif file == '.txt':
            loader = txt_loader(uploaded_file.name)
        elif file == '.csv':
            loader = csv_loader(uploaded_file.name)
        else:
            st.warning('Please Provide valid Document type (PDF, TXT, CSV)')

        data = Text_Splitter(loader)
        st.write(data)

        embeding_model = st.sidebar.radio('Select Embedding Model',options=['OpenAI','Google Gemini','HuggingFace'])
        st.write(embeding_model)

        store = st.sidebar.radio('Select Vector Store',options=['FAISS','Chroma','InMemoryVectorStore'])
        st.write(store)

        vector_store = Generate_embeddings(data,embeding_model,store)

        query = st.text_input('Ask Your Query from Document')

        try:
            response = vector_store.similarity_search(query)
            st.write(response)

        except Exception as e:
            st.write(f'Error : {e}')

