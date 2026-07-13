from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser,PydanticOutputParser
from pydantic import BaseModel,Field
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langserve import add_routes
from fastapi import FastAPI
import streamlit as st

load_dotenv()

app = FastAPI()

@app.get('/health')
def health():
    return {'message':'I am healthy'}

class QA(BaseModel):
    Question : str = Field(description='Return only the Question')
    Answer : str = Field(description='Return only the Answer')

@app.post('/chat')
def chatbot(request:QA):

    llm = ChatGroq(model='llama-3.1-8b-instant')
    parser = PydanticOutputParser(pydantic_object=QA)
    prompt = PromptTemplate(template='You are an helpfull Assistant. Answer the Query {question}',input_variables=['question'])

    chain = prompt | llm | parser

    response = chain.invoke({'question':request.Question})

    return {'answer':response}
