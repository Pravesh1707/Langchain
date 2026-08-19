from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool 
from typing import Union
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from dotenv import load_dotenv
import ast
import operator as op

load_dotenv()


_ops = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod
}

def  eval_node(node) -> Union[int,float]:
    if isinstance(node,ast.Constant) and isinstance(node.value,(int,float)):
        return node.value
    if isinstance(node,ast.BinOp) and type(node.op) in _ops:
        return _ops[type(node.op)](eval_node(node.left),eval_node(node.right))
    raise ValueError("Unsupported expression. Use numbers, + - * / // % **")

def safe_Calc(exp : str) -> float:
    exp = exp.strip()
    if len(exp) == 0 or len(exp)>200:
        raise ValueError("Expression is short or too long")
    tree = ast.parse(exp,mode='eval')
    return float(eval_node(tree.body))

@tool
def calculate(expression:str)->str:
    """safely evaluate arithmetic expression like (2+5) or (345*123)+21-32. Return only the number."""
    try:
        answer = safe_Calc(expression)
        if abs(answer)>1e18:
            return "Error : Answer to large"
        return str(int(answer)) if answer.is_integer() else str(answer)
    except Exception as e:
        return f"Error : {e}"

def build_calc_agent():
    model = ChatOpenAI(model="gpt-4o")
    tool = [calculate]
    prompt = ChatPromptTemplate.from_messages([("system","You are a precise math asssistant\n"
    "RULES:\n"
    "1. Always use the 'calculate tool for arithmatic; do not compute by yourself.\n"
    "2. Convert natural language to a clean math expression"
    "\n    -if user writes '^' for exponent, convert to '**'.\n"
    "3. Keep expression short and safe."),("human","{input}")])

    agent = create_tool_calling_agent(llm=model,tools=tool,prompt=prompt)
    return AgentExecutor(agent=agent,tools=tool,verbose=False)

calc_agent = build_calc_agent()

query = input("Enter your expression : ")
while not query == "exit":
    result = calc_agent.invoke({"input":query})
    print(result["output"])
    query = input("Enter your next Query : ")
