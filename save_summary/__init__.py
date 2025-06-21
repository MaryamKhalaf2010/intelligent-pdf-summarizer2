import os
import logging
from azure.storage.blob import BlobServiceClient

# 🔁 Load connection string from env
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AzureWebJobsStorage")

# 🔁 Replace UseDevelopmentStorage=true with actual Azurite connection string
if AZURE_STORAGE_CONNECTION_STRING == "UseDevelopmentStorage=true":
    AZURE_STORAGE_CONNECTION_STRING = (
        "DefaultEndpointsProtocol=http;"
        "AccountName=devstoreaccount1;"
        "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
        "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    )

OUTPUT_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_OUTPUT", "output")

def main(input_data: dict):
    # ✅ Extract info safely
    summary_text = input_data["summary"]
    original_filename = input_data["filename"]

    # ✅ Generate output filename
    output_filename = original_filename.replace(".pdf", "-summary.txt")

    try:
        # ✅ Upload to Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(OUTPUT_CONTAINER_NAME)

        # Ensure the output container exists
        try:
            container_client.create_container()
        except Exception:
            pass  # ignore if already exists

        container_client.upload_blob(name=output_filename, data=summary_text, overwrite=True)
        logging.info(f"✅ Summary saved to blob: {output_filename}")
    except Exception as e:
        logging.error(f"❌ Failed to save summary: {e}")
        raise
