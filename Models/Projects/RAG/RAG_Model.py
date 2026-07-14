
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma.vectorstores import Chroma

# from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
import streamlit as st 
from dotenv import load_dotenv

load_dotenv()


def get_response(query):

    llm = ChatGroq(model='llama-3.1-8b-instant')
    prompt = ChatPromptTemplate.from_template(''' Answer from the following context only and provide he msot accurate result based on the context only.
                                          {context}
                                          
                                          Question : {input}''')
    chain = create_stuff_documents_chain(llm,prompt)

    finalchain = create_retrieval_chain(st.session_state.retriver ,chain)
    response  = finalchain.invoke({'input':query})
    return response

def generate_embedings():
    if "vectors" not in st.session_state:
        st.session_state.embedings = OpenAIEmbeddings()
        st.session_state.loader = PyPDFDirectoryLoader('Data')
        st.session_state.docs = st.session_state.loader.load()
        st.session_state.splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
        st.session_state.chunks = st.session_state.splitter.split_documents(st.session_state.docs )
        st.session_state.vector = Chroma.from_documents(st.session_state.chunks,st.session_state.embedings)
        st.session_state.retriver = st.session_state.vector .as_retriever()
        st.write('Vector Embeddings Done !')

st.title('GROQ RAG Model')
st.write('Click the Buttion to Generate Embedings')
if st.button('Generate Embeddings'):
    generate_embedings()


query = st.text_input("Ask your query from the Document")
if st.button('Answer'):
    if query:
        response = get_response(query)
        st.write(response['answer'])
        with st.expander('Reference :'):
            if 'context' in response:
                for i,doc in enumerate(response['context']):
                    st.write(doc.page_content)
                    st.write('-----------------------------------------')
