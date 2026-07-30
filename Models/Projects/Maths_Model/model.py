# For UI
import streamlit as st 

# LLM / Models 
from langchain_groq import ChatGroq
# from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Prompt
from langchain_core.prompts import PromptTemplate

#chains
from langchain_classic.chains.llm_math.base import LLMMathChain
from langchain_classic.chains.llm import LLMChain
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun

from langchain_classic.agents.agent_types import AgentType
# from langchain_core.tools import Tool
from langchain_classic.agents import initialize_agent,Tool
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
import re

load_dotenv()

# pip install wikipedia


st.title("Maths Problem solver Chat Bot")

sidebar = st.sidebar

sidebar.title("Settings")
grok_apikey = sidebar.text_input("Enter your GROQ API KEY",type="password")
if not grok_apikey:
    st.info("Please enter the api key")
    st.stop()

model = ChatGroq(model='llama-3.1-8b-instant',api_key=grok_apikey)

wikipedia = WikipediaAPIWrapper(wiki_client=any)

wiki_tool = Tool(
    func=wikipedia.run,name="Wiki Tool",description="Tool is used for searching over the internet to find various informations"
)

math_chain = LLMMathChain.from_llm(llm=model)

def math_tool(question):
    math_ex = ''.join(re.findall(r'[\d.+*/^()-]+',question))
    return math_chain.run(math_ex)

calculate = Tool(
    name="calculator",
    func=math_tool,
    description="Tool is used to answering maths related questions. Only input mathematics expression needed"
)

prompt = PromptTemplate(template='''You are an agent tasked with solving user mathematical problem. 
Logically arrived at the solution and display it point wise for the question below:
Question : {question}
Answer : ''',input_variables=['question'])

chain = LLMChain(llm=model,prompt=prompt)
# chain = prompt | model

Reasoning = Tool(
    name="Reasoning",
    func=chain.run,
    description="A Tool used for answering logic based and reasoning questions"
)

assistant = initialize_agent(
    tools=[wiki_tool,calculate,Reasoning],
    llm=model,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose = False,
    handle_parsing_errors=True
)

if "message" not in st.session_state:
    st.session_state['message'] = [{'role':'assistant','content':"Hi i am an AI Assistant who can solve your Maths & Reasoning Question"}]

for msg in st.session_state['message']:
    st.chat_message(msg['role']).write(msg['content'])

query = st.text_input("Please Ask your Question.....")

answer = st.button('Find Answer')

if answer:
    if query:
        with st.spinner('Generating Response....'):
            st.session_state.message.append({'role':'user','content':query})
            st.chat_message('user').write(query)

        if re.search(r'[\d.+*/^()-]+',query):
            response = calculate.run(query)
        else:
            st_cb = StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            response = assistant.run(query,callbacks=[st_cb])
        st.session_state.message.append({'role':'assistant','content':response})
        st.chat_message('assistant').write(response)
    else:
        st.warning("Please enter the Question")
