# utility_functions.py

import requests
import time
import json
import os

def send_pii_detection_request(text_content, document_id, api_key, api_endpoint, api_version="2023-04-15-preview", show_stats="True"):
    """
    Sends a PII detection request for a single document.

    Parameters:
        text_content (str): The text content.
        document_id (str): Unique identifier for the text.
        api_key (str): Azure subscription key.
        api_endpoint (str): The endpoint URL for the API (should include 'language/analyze-text/jobs').
        api_version (str): API version.
        show_stats (str): Whether to include document and transaction counts in the response.

    Returns:
        str: Operation location if the request is accepted, None otherwise.
    """
    documents = [{
        "id": str(document_id),
        "language": "en",
        "text": text_content
    }]

    payload = {
        "displayName": f"PII Detection Task for {document_id}",
        "analysisInput": {
            "documents": documents
        },
        "tasks": [
            {
                "kind": "PiiEntityRecognition",
                "taskName": f"PII Detection Task {document_id}",
                "parameters": {
                    "model-version": "latest",
                    "piiCategories": ["Person", "URL", "Email", "PhoneNumber"]
                }
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key
    }

    try:
        response = requests.post(
            f"{api_endpoint}?api-version={api_version}&showStats={show_stats}",
            headers=headers,
            data=json.dumps(payload)
        )

        if response.status_code == 202:
            operation_location = response.headers.get("operation-location")
            print(f"Request for document ID {document_id} accepted.")
            print(f"Operation Location: {operation_location}")
            return operation_location
        else:
            print(f"Failed to submit request for document ID {document_id}. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"Exception occurred while sending request for document ID {document_id}: {str(e)}")
        return None

def save_table(table, file_path):
    """
    Saves a table (dictionary) to a JSON file.

    Parameters:
        table (dict): The table to save.
        file_path (str): The path where the table will be saved.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(table, f, ensure_ascii=False, indent=4)
    print(f"Table saved to {file_path}")

def load_table(file_path):
    """
    Loads a table (dictionary) from a JSON file.

    Parameters:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The loaded table.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        table = json.load(f)
    print(f"Table loaded from {file_path}")
    return table

def check_all_jobs_finished(operation_table, api_key):
    """
    Checks if all jobs in the operation table are finished.

    Parameters:
        operation_table (dict): Mapping from document IDs to operation locations.
        api_key (str): Azure subscription key.

    Returns:
        bool: True if all jobs are finished, False otherwise.
    """
    headers = {
        "Ocp-Apim-Subscription-Key": api_key
    }

    all_finished = True
    for doc_id, operation_location in operation_table.items():
        try:
            response = requests.get(operation_location, headers=headers)
            if response.status_code == 200:
                job_status = response.json().get("status")
                print(f"Job Status for Document ID {doc_id}: {job_status}")

                if job_status in ["notStarted", "running"]:
                    all_finished = False
            else:
                print(f"Failed to get job status for Document ID {doc_id}. Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                all_finished = False
        except Exception as e:
            print(f"Exception occurred while checking job status for Document ID {doc_id}: {str(e)}")
            all_finished = False

    return all_finished

def retrieve_all_results(operation_table, api_key):
    """
    Retrieves results for all completed jobs in the operation table.

    Parameters:
        operation_table (dict): Mapping from document IDs to operation locations.
        api_key (str): Azure subscription key.

    Returns:
        dict: Mapping from document IDs to their processed results.
    """
    headers = {
        "Ocp-Apim-Subscription-Key": api_key
    }

    results_table = {}
    for doc_id, operation_location in operation_table.items():
        try:
            response = requests.get(operation_location, headers=headers)
            if response.status_code == 200:
                job_results = response.json()
                entities = process_results(job_results, doc_id)
                results_table[doc_id] = entities
                print(f"Results retrieved for Document ID {doc_id}.")
            else:
                print(f"Failed to retrieve results for Document ID {doc_id}. Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                results_table[doc_id] = None
        except Exception as e:
            print(f"Exception occurred while retrieving results for Document ID {doc_id}: {str(e)}")
            results_table[doc_id] = None

    return results_table

def process_results(job_results, doc_id):
    """
    Processes the job results and structures them into a list of entities.

    Parameters:
        job_results (dict): JSON response from the job results.
        doc_id (str): The document ID corresponding to the results.

    Returns:
        list: List of entities with fields [entity_text, type, positions].
    """
    processed_data = []

    tasks = job_results.get("tasks", {})
    items = tasks.get("items", [])

    for task in items:
        results = task.get("results", {})
        documents = results.get("documents", [])

        for doc in documents:
            if doc.get("id") == doc_id:
                entities = doc.get("entities", [])

                for entity in entities:
                    entity_text = entity.get("text")
                    entity_type = entity.get("category")
                    offset = entity.get("offset")
                    length = entity.get("length")
                    positions = (offset, offset + length)

                    processed_data.append({
                        "entity_text": entity_text,
                        "type": entity_type,
                        "positions": positions
                    })
    return processed_data
