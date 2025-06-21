import os
from azure.storage.blob import BlobServiceClient

# ✅ Use local Azurite connection string
connection_str = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)
container_name = "input"
blob_name = "sample.pdf"
file_path = "sample.pdf"

# ✅ Create BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_str)
container_client = blob_service_client.get_container_client(container_name)

# ✅ Upload PDF
with open(file_path, "rb") as data:
    container_client.upload_blob(name=blob_name, data=data, overwrite=True)
    print(f"✅ Uploaded '{blob_name}' to container '{container_name}'")
