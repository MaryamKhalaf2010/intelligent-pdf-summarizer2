import os
import logging
import json
import azure.functions as func
import azure.durable_functions as df
import requests
from azure.storage.blob import BlobServiceClient

# Load environment variables
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
BLOB_CONTAINER_INPUT = os.getenv("BLOB_CONTAINER_INPUT")
BLOB_CONTAINER_OUTPUT = os.getenv("BLOB_CONTAINER_OUTPUT")

# Orchestrator function
def orchestrator_function(context: df.DurableOrchestrationContext):
    blob_info = context.get_input()
    text = yield context.call_activity("extract_text", blob_info)
    summary = yield context.call_activity("summarize_text", text)
    yield context.call_activity("save_summary", {"summary": summary, "blob": blob_info})
    return summary

main = df.Orchestrator.create(orchestrator_function)

# Activity: extract_text (dummy text)
def extract_text_activity(blob_info: dict) -> str:
    logging.info(f"🔍 Extracting text from: {blob_info['filename']}")
    return "This is dummy text extracted from a PDF document for testing."

# Activity: summarize_text
def summarize_text_activity(text: str) -> str:
    url = f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2024-03-01"
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_KEY
    }
    payload = {
        "messages": [{"role": "user", "content": f"Summarize this text: {text}"}],
        "temperature": 0.7,
        "max_tokens": 200
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# Activity: save_summary
def save_summary_activity(data: dict):
    connect_str = os.getenv("AzureWebJobsStorage")
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    output_container_client = blob_service_client.get_container_client(BLOB_CONTAINER_OUTPUT)

    filename = data['blob']['filename'].replace(".pdf", "-summary.txt")
    output_blob = output_container_client.get_blob_client(filename)
    output_blob.upload_blob(data['summary'], overwrite=True)
    logging.info(f"✅ Summary saved as: {filename}")

# Function entry points
def extract_text(req: func.ActivityTrigger) -> str:
    return extract_text_activity(req)

def summarize_text(req: func.ActivityTrigger) -> str:
    return summarize_text_activity(req)

def save_summary(req: func.ActivityTrigger):
    save_summary_activity(req)
    return "Done"

app = func.FunctionApp()

app.activity_trigger(name="extract_text")(extract_text)
app.activity_trigger(name="summarize_text")(summarize_text)
app.activity_trigger(name="save_summary")(save_summary)
app.orchestration_trigger(context_name="context")(main)
