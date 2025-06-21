import logging
import azure.functions as func
import azure.durable_functions as df

async def main(blob: func.InputStream, starter: str):
    client = df.DurableOrchestrationClient(starter)

    blob_info = {
        "filename": blob.name.split("/")[-1],
        "size": blob.length
    }

    logging.info(f"📥 New blob detected: {blob.name}, Size: {blob.length} bytes")

    # ✅ Await the orchestration start
    instance_id = await client.start_new("orchestrator", None, blob_info)

    logging.info(f"✅ Started orchestration with ID = '{instance_id}'")
