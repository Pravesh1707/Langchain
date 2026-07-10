import streamlit as st 
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()


st.title("Simple chat bot")

role = st.selectbox('Select Role',['AI Engineer','Data Scientist','Data Engineer'])

goal = st.text_input("What Goal you have in Mind")

context = st.text_area("Tell me about your experience")

template = PromptTemplate(template=""" You are an Senior {role} working in a 
                        company. You always have a {goal} in mind and you have {context} """,
                        input_variables=['role','goal','context'],validate_template=True)

prompt = template.invoke({'role':role,'goal':goal,'context':context})

model = ChatOpenAI(model='gpt-3.5-turbo')

response = model.invoke(prompt)

if st.button("Answer"):
    st.write(response.content)