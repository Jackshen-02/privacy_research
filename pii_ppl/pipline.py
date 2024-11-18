# pipeline.py

import json
import os
import time
from utility_functions import (
    send_pii_detection_request,
    save_table,
    load_table,
    check_all_jobs_finished,
    retrieve_all_results
)

def process_texts(text_list, identifier_list, storage_directory):
    # Load API credentials
    with open('input/secret.json', 'r', encoding='UTF-8') as file:
        secret_json = json.load(file)
    API_KEY = secret_json['LANGUAGE_KEY']
    API_ENDPOINT = secret_json['LANGUAGE_ENDPOINT'] + 'language/analyze-text/jobs'

    if not text_list or not identifier_list:
        print("No texts or identifiers were provided. Exiting.")
        return

    if len(text_list) != len(identifier_list):
        print("The number of texts and identifiers must be the same.")
        return

    if not os.path.exists(storage_directory):
        os.makedirs(storage_directory)
        print(f"Directory '{storage_directory}' created.")

    # Initialize rate limiting variables
    max_requests_per_second = 100
    max_requests_per_minute = 1000
    requests_in_current_second = 0
    requests_in_current_minute = 0
    second_start_time = time.time()
    minute_start_time = time.time()

    operation_table = {}
    unique_identifier = os.path.basename(storage_directory)

    total_texts = len(text_list)

    for idx, (text_content, document_id) in enumerate(zip(text_list, identifier_list)):
        current_time = time.time()

        # Check per-minute rate limit
        elapsed_minute = current_time - minute_start_time
        if elapsed_minute >= 60:
            # Reset minute counters
            requests_in_current_minute = 0
            minute_start_time = current_time
        elif requests_in_current_minute + 1 > max_requests_per_minute:
            # Sleep until the next minute
            sleep_time = 60 - elapsed_minute
            print(f"Reached per-minute rate limit. Sleeping for {sleep_time:.2f} seconds.")
            time.sleep(sleep_time)
            # Reset minute counters after sleep
            requests_in_current_minute = 0
            minute_start_time = time.time()

        # Check per-second rate limit
        elapsed_second = current_time - second_start_time
        if elapsed_second >= 1:
            # Reset second counters
            requests_in_current_second = 0
            second_start_time = current_time
        elif requests_in_current_second + 1 > max_requests_per_second:
            # Sleep until the next second
            sleep_time = 1 - elapsed_second
            print(f"Reached per-second rate limit. Sleeping for {sleep_time:.2f} seconds.")
            time.sleep(sleep_time)
            # Reset second counters after sleep
            requests_in_current_second = 0
            second_start_time = time.time()

        # Send PII detection request for the current text
        operation_location = send_pii_detection_request(
            text_content=text_content,
            document_id=document_id,
            api_key=API_KEY,
            api_endpoint=API_ENDPOINT
        )

        if operation_location is None:
            print(f"Failed to submit request for document ID {document_id}.")
            continue

        # Update operation table
        operation_table[document_id] = operation_location

        # Update rate limiting counters
        requests_in_current_second += 1
        requests_in_current_minute += 1

        # Sleep briefly to avoid hitting the per-second limit in tight loops
        time.sleep(0.01)  # Sleep for 10 milliseconds

    # Save operation table
    operation_table_path = os.path.join(storage_directory, f"{unique_identifier}_operation_table.json")
    save_table(operation_table, operation_table_path)

    # Save text_list and identifier_list for later use
    text_list_path = os.path.join(storage_directory, f"{unique_identifier}_text_list.json")
    save_table(text_list, text_list_path)

    identifier_list_path = os.path.join(storage_directory, f"{unique_identifier}_identifier_list.json")
    save_table(identifier_list, identifier_list_path)

    print(f"Operation table, text list, and identifier list saved to {storage_directory}")
    return operation_table_path

def check_jobs_and_retrieve_results(storage_directory):
    # Load API credentials
    with open('input/secret.json', 'r', encoding='UTF-8') as file:
        secret_json = json.load(file)
    API_KEY = secret_json['LANGUAGE_KEY']

    unique_identifier = os.path.basename(storage_directory)
    operation_table_path = os.path.join(storage_directory, f"{unique_identifier}_operation_table.json")
    if not os.path.exists(operation_table_path):
        print(f"Operation table not found at {operation_table_path}")
        return

    # Load operation table
    operation_table = load_table(operation_table_path)
    all_finished = check_all_jobs_finished(operation_table, API_KEY)
    if not all_finished:
        print("Some jobs are still in progress. Please try again later.")
        return

    # Retrieve results
    results_table = retrieve_all_results(operation_table, API_KEY)

    # Load text_list and identifier_list
    text_list_path = os.path.join(storage_directory, f"{unique_identifier}_text_list.json")
    identifier_list_path = os.path.join(storage_directory, f"{unique_identifier}_identifier_list.json")

    if os.path.exists(text_list_path) and os.path.exists(identifier_list_path):
        text_list = load_table(text_list_path)
        identifier_list = load_table(identifier_list_path)
    else:
        print(f"Text list or identifier list not found in {storage_directory}")
        return

    # Map identifiers to their corresponding texts and labels
    text_label_table = {}
    for doc_id, entities in results_table.items():
        index = identifier_list.index(doc_id)
        text = text_list[index]
        text_label_table[doc_id] = {
            "text": text,
            "entities": entities
        }

    # Save the results
    results_table_path = os.path.join(storage_directory, f"{unique_identifier}_results.json")
    save_table(text_label_table, results_table_path)
    print(f"Results saved to {results_table_path}")
    return results_table_path

# if __name__ == "__main__":
#     # Example usage:

#     # Provide the list of texts
#     text_list = [
#         "John Doe's email is john.doe@example.com.",
#         "Visit https://www.example.com for more info.",
#         # Add more texts as needed
#     ]

#     # Provide a corresponding list of unique identifiers for each text
#     identifier_list = [
#         "doc1",
#         "doc2",
#         # Add more identifiers as needed
#     ]

#     # Provide the directory to store the tables
#     storage_directory = "output/batch1"

#     # Process the texts
#     process_texts(text_list, identifier_list, storage_directory)

#     # Wait for processing (e.g., time.sleep(60)) if needed

#     # Check if all jobs are finished and retrieve results
#     check_jobs_and_retrieve_results(storage_directory)
