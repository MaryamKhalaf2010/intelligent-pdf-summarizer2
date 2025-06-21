import os
import requests
import logging

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
DEPLOYMENT_NAME = os.getenv("CHAT_MODEL_DEPLOYMENT")  

def main(text: str) -> str:
    url = f"{AZURE_OPENAI_ENDPOINT.rstrip('/')}/openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version=2025-01-01-preview"

    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_KEY
    }
    payload = {
        "messages": [{"role": "user", "content": f"Summarize this text: {text}"}],
        "temperature": 0.7,
        "max_tokens": 300
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        summary = response.json()["choices"][0]["message"]["content"]
        logging.info("Summary created successfully.")
        return summary
    except Exception as e:
        logging.error(f" Failed to summarize text: {e}")
        raise
