# core/llm.py
import requests
from config.system_prompt import SYSTEM_PROMPT

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:7b"

def chat_with_llm(user_input: str) -> str:
    """
    Send text to LLM and return response string.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]
    
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()["message"]["content"]
    except Exception as e:
        return f"Ugh. My brain froze. ({e})"