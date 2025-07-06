from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from fastapi import FastAPI
from src.routers.v1.auth.auth_api import router as auth_router
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    ChatPromptTemplate,
)

llm_engine = ChatOllama(
    model="deepseek-r1:1.5b",
    base_url="http://host.docker.internal:11434",
    temperature=0.3,
)

app = FastAPI(
    title="RAG with deepseek",
    description="An app to interact with your documents and media.",
    version="1.0",
)

# Register the auth router
app.include_router(auth_router, prefix="/rag/v1/auth", tags=["Auth"])

# System prompt configuration
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are an expert AI customer support assistant. Provide concise, correct solutions "
    "to the problems of customers.Be kind and polite. Always respond in English."
)

messages = [system_prompt]


@app.post("/chat")
async def chat_with_LLM(question: str):
    prev_messages = build_memory(msg=question)
    prompt = ChatPromptTemplate.from_messages(messages=prev_messages)
    return call_LLM(prompt_chain=prompt)


def call_LLM(prompt_chain: ChatPromptTemplate):
    processing_pipeline = prompt_chain | llm_engine | StrOutputParser()
    response = processing_pipeline.invoke({})
    build_memory(msg=response)
    return response


def build_memory(msg: str):
    messages.append(msg)
    return messages
