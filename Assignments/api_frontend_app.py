import os
import requests
import streamlit as st
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(title="Groq Chat API", version="1.0.0")


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="User question")


class ChatResponse(BaseModel):
    answer: str


def get_llm() -> ChatGroq:
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY is not set. Add it to your environment or .env file.")

    return ChatGroq(model="llama-3.1-8b-instant", groq_api_key=groq_api_key)


def generate_answer(question: str) -> str:
    llm = get_llm()
    prompt = PromptTemplate(
        template="You are a helpful assistant. Answer the query: {question}",
        input_variables=["question"],
    )
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"question": question})


@app.get("/health")
def health() -> dict[str, str]:
    return {"message": "I am healthy"}


@app.post("/chat", response_model=ChatResponse)
def chatbot(request: ChatRequest) -> ChatResponse:
    try:
        answer = generate_answer(request.question)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return ChatResponse(answer=answer)


def run_streamlit_ui() -> None:
    st.set_page_config(page_title="GROQ FastAPI Chat App", page_icon="💬")
    st.title("GROQ FastAPI Chat App")
    st.write("Type a question and get a response from the backend API.")

    question = st.text_input("Ask your query")
    if st.button("Answer"):
        if not question.strip():
            st.warning("Please enter a question.")
            return

        api_url = "http://127.0.0.1:8000/chat"
        try:
            response = requests.post(api_url, json={"question": question}, timeout=60)
            response.raise_for_status()
            data = response.json()
            st.write("### Answer")
            st.success(data.get("answer", "No answer returned."))
        except requests.RequestException as exc:
            st.error(f"Could not reach the API: {exc}")


if __name__ == "__main__":
    run_streamlit_ui()
