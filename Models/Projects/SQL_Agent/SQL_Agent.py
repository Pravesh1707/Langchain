import streamlit as st 
from pathlib import Path
from langchain_community.callbacks.streamlit import streamlit_callback_handler
from langchain_classic.agents.agent_types import AgentType
from langchain_classic.agents.agent_toolkits import create_sql_agent
from langchain_classic.agents.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv


load_dotenv()

st.title('Langchain : Chat with SQL')

LOCALDB ='USE_LOCALDB'
MYSQLDB ='USE_MYSQL'

radio_opt = ['USE SQLite3 DB(Student.db)','Connect to MySQL DB']
radio_btn = st.sidebar.radio('choose the DB yo want to Chat with',options=radio_opt)
if radio_btn =='Connect to MySQL DB':
    db_uri = MYSQLDB
    mysql_host = st.sidebar.text_input('Provide MySQL Hostname', value='localhost')
    mysql_user = st.sidebar.text_input('Provide MySQL Username', value='root')
    mysql_user = st.sidebar.text_input('Provide MySQL Password', value='password')
    mysql_db = st.sidebar.text_input('Provide MySQL Database Name')
else:
    db_url = LOCALDB

groq_api = st.sidebar.text_input('Provide with the GROQ API Key : ',type='password')

if not groq_api:
    st.info('Please Provide your Groq API key ')
    st.stop()

model = ChatGroq(model='llama-3.1-8b-instant',api_key=groq_api,streaming=True)

@st.cache_resource(ttl=7200)
def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_password=None,mysql_db=None):

    if db_uri == LOCALDB:
        db_file_path = (Path(__file__).parent/'student.db').absolute()
        create = lambda : sqlite3.connect(f"File:{db_file_path}?mode='ro",uri=True)
        return SQLDatabase(create_engine("sqlite:///",creator=create))
    
    elif db_uri == MYSQLDB:
        if not(mysql_host and mysql_password not mysql_user and mysql_db):
            st.error("Please Provide all MYSQL Connection Details")
            st.stop()

        encoded_pass = quote_plus(mysql_password)
        connection_str = f"mysql+mysqlconnetor://{mysql_user}:{encoded_pass}@{mysql_host}/{mysql_db}"

        try:
            db_sql_DB = SQLDatabase(create_engine(connection_str))
            st.success("MYSQL Successfuly Connected")
            return db_sql_DB
        
        except Exception as e:
            st.error(f'Failed to connect to MYSQL :{e}')
            st.stop()

