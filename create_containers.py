import os
from azure.storage.blob import BlobServiceClient

# ✅ Explicit Azurite connection string
connection_str = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

input_container = "input"
output_container = "output"

try:
    blob_service_client = BlobServiceClient.from_connection_string(connection_str)

    for container_name in [input_container, output_container]:
        try:
            blob_service_client.create_container(container_name)
            print(f"✅ Created container: {container_name}")
        except Exception as e:
            print(f"ℹ️ Container {container_name} may already exist: {e}")
except Exception as e:
    print(f"❌ Failed to connect to Azurite: {e}")
