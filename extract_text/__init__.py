import logging

def main(blob_info: dict) -> str:
    logging.info(f"🔍 Extracting text from: {blob_info['filename']}")
    return "This is dummy text extracted from a PDF document for testing."
