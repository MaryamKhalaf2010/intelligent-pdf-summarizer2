
# Intelligent PDF Summarizer (Azure Durable Functions Lab)

This project is a serverless application built with **Azure Durable Functions**, designed to automatically **extract and summarize content from uploaded PDF files**. The resulting summary is then saved to Azure Blob Storage for retrieval.

---

## Features

-  **Blob-triggered Durable Function** to start processing on file upload  
-  **Form Recognizer** (or mocked) extracts text from the PDF  
-  **Azure OpenAI** (or mocked) summarizes the extracted text  
-  Final summary is saved as a `.txt` file to the output Blob container  

---

## Technologies Used

- Azure Functions (Python)  
- Azure Durable Functions  
- Azure Blob Storage  
- **Azurite** (for local emulation of Blob storage)  
- Azure OpenAI (Mocked in this implementation)  
- Azure CLI / Azure Developer CLI (`azd`)  
- Bicep (Infrastructure as Code)  

---

## Project Structure

```
intelligent-pdf-summarizer2/
│
├── extract_text/              # Activity function: Form Recognizer or mock
├── summarize_text/            # Activity function: Azure OpenAI or mock
├── save_summary/              # Activity function: Save result to Blob
├── orchestrator/              # Orchestration logic chaining the steps
├── process_document/          # Blob trigger to start pipeline
├── upload_pdf_to_blob.py      # Script to upload sample PDF
├── create_containers.py       # Script to create Azurite containers
├── local.settings.json        # Local config including environment variables
├── requirements.txt
├── infra/                     # Infrastructure folder (Bicep templates)
└── README.md
```

---

## How It Works (Locally)

1. **Run Azurite**  
   ```bash
   npx azurite --silent --location ./azurite --debug ./azurite/debug.log
   ```

2. **Start the Azure Function App locally**  
   ```bash
   func start --port 7072
   ```

3. **Upload a sample PDF**  
   ```bash
   python3 upload_pdf_to_blob.py
   ```

4. Watch logs to see:  
   - PDF is detected  
   - Text extracted (mocked)  
   - Summary generated (mocked)  
   - Summary saved as `sample-summary.txt` in the output container  

---

## About Azure Quota Limitations

Due to Azure OpenAI and App Service plan quota restrictions on student accounts:

- The actual call to Azure OpenAI was **mocked** as instructed by the professor.
- Azure deployment using `azd up` failed repeatedly due to:
  - `SubscriptionIsOverQuotaForSku`
  - No Dynamic/Free SKU availability in selected regions
- The entire Durable Functions flow was tested locally using Azurite.

---

##  Mock Summarization Code (in `summarize_text/__init__.py`)

```python
def main(text: str) -> str:
    logging.info(" [MOCK] Skipping OpenAI and returning a fake summary.")
    return "This is a mock summary of the uploaded PDF content."
```

---

##  Status

- [x] Local execution works end-to-end  
- [x] Blob trigger activates on PDF upload  
- [x] Mocked AI summary created  
- [x] Summary saved to output Blob container  
- [x] Cloud deployment

---
## Video
https://youtu.be/sZZuonY9gyI

##  Author

**Maryam Khalaf**  
Algonquin College – CST8919  
GitHub: [@MaryamKhalaf2010](https://github.com/MaryamKhalaf2010)
