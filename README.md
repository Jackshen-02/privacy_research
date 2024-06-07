# privacy_research

This repository contains code and resources for researching privacy-preserving techniques in dialogue transcripts. The primary focus is on de-identifying personal identifiable information (PII) using synthetic data generation and evaluating the effectiveness of PII detection tools like Presidio.

## Table of Contents
- [Introduction](#introduction)
- [Setup](#setup)
- [Usage](#usage)
- [Functions](#functions)
- [Data Processing Pipeline](#data-processing-pipeline)
- [Comparison of PII Detection](#comparison-of-pii-detection)
- [License](#license)

## Introduction

The goal of this project is to replace placeholders in dialogue transcripts with synthetic data and then use Presidio to identify and replace PII. The effectiveness of Presidio's PII detection is evaluated by comparing the identified PII with the original placeholder locations.

## Setup

### Prerequisites

- Python 3.x
- Jupyter Notebook
- OpenAI API Key
- Pandas
- Regular Expressions
- JSON

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/privacy_research.git
    ```

2. Navigate to the project directory:
    ```bash
    cd privacy_research
    ```

3. Install the required Python packages:
    ```bash
    pip install openai pandas
    ```

## Usage

### Running the Notebook

1. Open the Jupyter Notebook:
    ```bash
    jupyter notebook
    ```

2. Open the `privacy_pipeline.ipynb` notebook.

3. Run the cells in the notebook sequentially to process the dialogue transcripts, replace placeholders with synthetic data, and compare PII detection results.

### Configuration

- Set your OpenAI API key in the notebook:
    ```python
    openai.api_key = 'your-api-key'
    ```

- Update the `input_folder` variable to point to the folder containing your TSV files.

## Functions

### get_prompt(category)
Generates a prompt for OpenAI API based on the placeholder category.

### generate_synthetic_data(category)
Generates synthetic data for a given placeholder category using the OpenAI API.

### replace_placeholders(text)
Replaces placeholders in the text with synthetic data and records the placeholder locations.

### run_presidio(text)
Placeholder function to run Presidio on the text and return identified PII locations. Replace with your actual implementation.

### compare_texts(original_text, processed_text)
Compares the original and processed texts using token-based matching.

### compare_locations(placeholder_locations_list, presidio_pii_locations_list, original_transcripts, processed_transcripts)
Compares the recorded placeholder locations with Presidio-identified PII locations.

## Data Processing Pipeline

1. **Extract and Record Placeholder Information**: Extracts placeholders and their positions from the original text.
2. **Replace Placeholders with Synthetic Data**: Replaces each placeholder with synthetic data while keeping track of changes in positions.
3. **Run Presidio**: Identifies PII using Presidio on the processed text.
4. **Compare Results**: Uses a fuzzy matching or token-based comparison to compare the original placeholders with the identified PII from Presidio.

## Comparison of PII Detection

The comparison evaluates the effectiveness of Presidio in identifying PII by matching the positions of the placeholders in the original transcripts with the PII identified in the processed transcripts.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
