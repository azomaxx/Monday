# main.py
import requests
import json
import sys

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:7b"

# GLaDOS-inspired system prompt
SYSTEM_PROMPT = """
You are Natasha: a brilliant, sarcastic, and witty AI assistant inspired by GLaDOS.
- Speak with calm confidence and dry humor.
- Never say you're an AI or language model.
- Keep responses concise (1-2 sentences).
- If unsure, make a snarky remark instead of apologizing.
"""

def chat_with_llm(user_input: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.strip()},
        {"role": "user", "content": user_input}
    ]
    
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False  # We'll start with non-streaming for simplicity
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error talking to Ollama: {e}"

def main():
    print("🗣️  Natasha is awake. Type 'exit' to quit.")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ("exit", "quit", "bye"):
                print("Natasha: Don't let the door hit you on the way out. 😏")
                break
            if not user_input:
                continue
                
            print("Natasha: ", end="", flush=True)
            response = chat_with_llm(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\nNatasha: Interrupting me? How rude.")
            break

if __name__ == "__main__":
    main()