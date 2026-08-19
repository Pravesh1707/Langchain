from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from langchain_classic.memory.buffer import ConversationBufferMemory

load_dotenv()


model = ChatOpenAI(model="gpt-4o")

memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="input",
    output_key="text",
    return_messages=True
)

prompt = PromptTemplate(template="Chat History: {chat_history}\n\n Human: {input}",input_variables=["input"],memory_template = memory)

conversation_chain = LLMChain(llm=model,prompt = prompt, memory = memory,output_key="text")

query = input("Enter your Query : ")
while not query == "exit":
    result = conversation_chain.invoke({"input":query})
    print(result["text"])
    query = input("Enter your next Query : ")