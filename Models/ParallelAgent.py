import streamlit as st 
from langchain_core.output_parsers import PydanticOutputParser,StrOutputParser
from langchain_core.runnables import RunnableParallel
from langchain_core.prompts import PromptTemplate
from typing import Literal
from pydantic import BaseModel,Field
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

st.title(" Parallel Chain Model")

topic = st.text_input('Type in your Question ?')

class QuestionAnswer(BaseModel):
    Question : str =Field(description='Return only the exact Question which is asked ')
    answer : str = Field(description='return Only the Answer')
    summary : str = Field(description='Only Return the summary from the Question asked')
    quiz : list[str] = Field(description='Only Return the 5 follow-up Question You are asking')

pyParser = PydanticOutputParser(pydantic_object=QuestionAnswer)

strrParser = StrOutputParser()

ans_prompt = PromptTemplate(template='Generate the Answer on the {topic}',input_variables=['topic'])
sum_prompt = PromptTemplate(template='Generate the Summary on the {topic} in bullet points',input_variables=['topic'])
quiz_prompt = PromptTemplate(template='Generate the follow up Questions on the {topic} for practice',input_variables=['topic'])

par_model_1 = ChatOpenAI(model='gpt-3.5-turbo')
par_model_2 = ChatOpenAI(model='gpt-4o')
par_model_3 = ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite')

par_chain_1 = ans_prompt | par_model_1 | strrParser
par_chain_2 = sum_prompt | par_model_2 | strrParser
par_chain_3 = quiz_prompt | par_model_3 | strrParser

parallel_chain = RunnableParallel({'answer':par_chain_1,'summary':par_chain_2,'quiz':par_chain_3})

final_model = ChatGoogleGenerativeAI(model='gemini-3.5-flash')
final_prompt = PromptTemplate(template='Marge the following {answer}, {summary} and {quiz} together and return the result in this {format}',input_variables=['answer','summary','quiz'],partial_variables={'format':pyParser.get_format_instructions})

single_chain = final_prompt | final_model | pyParser
final_chain = parallel_chain | single_chain

parallel_chain_resul= final_chain.invoke({'topic':topic})

if st.button("Answer"):
    st.write(parallel_chain_resul)