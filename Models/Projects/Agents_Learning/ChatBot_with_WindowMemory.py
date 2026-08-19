from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.chains import LLMChain
from dotenv import load_dotenv
from langchain_classic.memory.buffer_window import ConversationBufferWindowMemory #memory window library


load_dotenv()

model = ChatOpenAI(model="gpt-4o")

memory = ConversationBufferWindowMemory(output_key="text",input_key="input",memory_key="chat_history",k=2) # K = Window length

prompt = PromptTemplate(template="Chat History : {chat_history}\n\n Human : {input}",input_variables=["input"],memory_template=memory)

chain = LLMChain(llm=model,prompt=prompt,memory=memory,output_key="text")

query = input("Enter your Query")

while query != "exit":
    result = chain.invoke({"input":query})
    print("AI : ",result["text"])
    query = input("Enter your Query")


