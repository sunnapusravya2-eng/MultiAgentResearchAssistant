from __future__ import annotations
from typing import Any
import os
from langchain_groq import ChatGroq

def create_llm() -> Any:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not configured in .env")
    return ChatGroq(model="llama-3.3-70b-versatile", api_key=api_key)