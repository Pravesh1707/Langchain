from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser,PydanticOutputParser
from pydantic import BaseModel,Field
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langserve import add_routes
from fastapi import FastAPI
import streamlit as st

load_dotenv()

api = FastAPI()

@api.get('/hello')
# @api_route('/hello')
def hello():
    return {'message':"Hello, how are you?"}


class TranslationRequest(BaseModel):
    lang : str
    text : str

@api.post('/llm')
def translate(request: TranslationRequest):
    prompt = PromptTemplate(template='Translate the text : {text} in {mentioned} language',input_variables=['text','mentioned'])

    llm = ChatGroq(model='llama-3.1-8b-instant')

    # parser = PydanticOutputParser(TranslationRequest)
    parser = StrOutputParser()

    chain = prompt | llm | parser

    response = chain.invoke({'text':request.text,'mentioned':request.lang})

    return {'Translation':response}


# class Hello(BaseModel):
#     name : str


# name = st.text_input("Enter your name")

# @api.post('./')
# def hello(request: Hello):
#     return get_hello(name)