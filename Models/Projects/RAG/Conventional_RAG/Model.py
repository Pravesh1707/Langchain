#LLM
from langchain_groq import ChatGroq

#RAG Requirements
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.history_aware_retriever import create_history_aware_retriever
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

#prompt
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import SystemMessage,AIMessage,HumanMessage

#UI
import streamlit as st 



def generate_embeddings(file):
    temp_file = './temporary.pdf'
    with open(temp_file,'wb') as f:
        f.write(file.getvalue())
    
    loader = PyPDFLoader(temp_file)
    doc = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000,chunk_overlap=500)
    chunks = splitter.split_documents(doc)
    Vector = Chroma.from_documents(chunks,embedding=OpenAIEmbeddings(),persist_directory="./chroma_db")
    retrever = Vector.as_retriever()

    st.write('Embeddings Created !')
    return retrever
        

def get_session_history(session_id):
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = ChatMessageHistory()
    return st.session_state.store[session_id]





def llm(model,query,retriever,session_id):
    # model = ChatGroq(model='llama-3.1-8b-instant')

    Hist_system_prompt = '''give a chat history and the latest user question, reformat the question to make it standalone. 
    Do not answer, 
    only rephrase.'''
    prompt = ChatPromptTemplate.from_messages([('system',Hist_system_prompt),MessagesPlaceholder('chat_history'),('human','{input}')])

    hist_chain = create_history_aware_retriever(model , retriever , prompt)

    system_prompt = '''You are an helpful AI assistant, For question answering, Answer from the provided context only. if unsure say, I don't know 
    context 
    {context}'''

    query_prompt = ChatPromptTemplate.from_messages([('system',system_prompt),MessagesPlaceholder('chat_history'),('human','{input}')])

    QA_chain = create_stuff_documents_chain(model, query_prompt)
    rga_chain = create_retrieval_chain(hist_chain,QA_chain)

    final_chain = RunnableWithMessageHistory(rga_chain,get_session_history,input_messages_key='input',
                                             history_messages_key='chat_history',output_messages_key='answer')
    response = final_chain.invoke({'input':query},config={'configurable':{'session_id':session_id}})
    return response




title = st.title('Conventional RAG ChaitBot')
api_key = st.text_input('Enter your API KEY',type='password')
if api_key:
    model = ChatGroq(model='llama-3.1-8b-instant',api_key=api_key)
    session_id = st.text_input('Enter your Session ID :',placeholder='abcd123..')
    if 'store' not in st.session_state:
        st.session_state.store ={}
    file = st.file_uploader('Please upload your file',type='pdf')
    if file :
        retriever = generate_embeddings(file)

        query = st.text_input('Ask Your Queary')
        if not query:
            st.warning('Please enter your query')
        if st.button('Answer'):
            session_hist = get_session_history(session_id)
            response = llm(model,query,retriever,session_id)
            st.subheader('Assistant Answer : ')
            st.write(response['answer'])

else:
    st.warning('Please Enter Valid API_KEY')


