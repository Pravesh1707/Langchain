import streamlit as st 
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

prompt = ChatPromptTemplate.from_messages([('system','You are a Helpful AI Assistant'),('human','Question : {question}')])

def get_response(query,llm,temperature,token):
    model = ChatOpenAI(model=llm,temperature=temperature,max_completion_tokens=token)

    parser = StrOutputParser()

    chain  = prompt | model | parser
    response = chain.invoke({'question':query})

    return response

query = st.text_input('Ask you Query')
llm = st.sidebar.title('Settings')
model = st.sidebar.selectbox('Select the Model : ',['gpt-3.5-turbo','gpt-4-turbo','gpt-4o','gpt-4o-mini'])
temperature = st.sidebar.slider('Select Temperature : ',max_value=2.0,min_value=0.0,value=0.5)
max_tokens = st.sidebar.slider('Select Max-Tokens : ',max_value=200,min_value=50,value=50)

if st.button('Answer'):
    if query:
        response = get_response(query,model,temperature,max_tokens)
        st.write(response)
    else:
        st.warning('Enter the query first')