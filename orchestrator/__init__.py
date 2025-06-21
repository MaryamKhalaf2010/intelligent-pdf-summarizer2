import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):
    # Get the blob information from the trigger (process_document)
    blob_info = context.get_input()  # Expected to be a dict like {"filename": "sample.pdf"}

    # Step 1: Extract text from the blob
    text = yield context.call_activity("extract_text", blob_info)

    # Step 2: Summarize the extracted text
    summary = yield context.call_activity("summarize_text", text)

    # Step 3: Save the summary with the original filename
    save_input = {
        "summary": summary,
        "filename": blob_info["filename"]
    }

    # Call save_summary with the correct structure
    yield context.call_activity("save_summary", save_input)

    # Optionally return the summary as a confirmation
    return summary

main = df.Orchestrator.create(orchestrator_function)

