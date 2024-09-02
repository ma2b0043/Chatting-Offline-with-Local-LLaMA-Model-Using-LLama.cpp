# Chatting with Local LLaMA Model Offline

## Overview

The **Chatting with Local LLaMA Model Offline** project is a Python-based application that integrates a quantized LLaMA model and Elasticsearch to enable efficient offline querying and response generation. This system allows users to interact with a local LLaMA model to obtain responses based on indexed textual data.

## Features

- **Quantized LLaMA Model:** Utilizes a quantized version of the LLaMA model for efficient text generation. For more details on the LLaMA model, visit [LLaMA CPP Python GitHub Repository](https://github.com/abetlen/llama-cpp-python).
- **Elasticsearch Integration:** Uses Elasticsearch for indexing and searching through textual data.
- **Python Libraries:** Incorporates essential libraries such as Sentence Transformers and Elasticsearch Python client.

## Installation

### Prerequisites

- **Python 3.8+**: Ensure you have Python 3.8 or later installed. You can download it from [Python Downloads](https://www.python.org/downloads/).

### Setting Up the Environment

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/your-repository.git
    cd your-repository
    ```

2. **Create and Activate Python Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Install Elasticsearch:**

    Download and install Elasticsearch from [Elasticsearch Downloads](https://www.elastic.co/downloads/elasticsearch). Follow the instructions to start the Elasticsearch service.

    ```bash
    ./bin/elasticsearch
    ```

    **Note:** Ensure that Elasticsearch is running on `http://localhost:9200` for the application to work correctly.

5. **Add the LLaMA Model File:**

    The project requires a quantized LLaMA model file to function. You need to download the model file (e.g., `model.gguf`) and place it in the `models/` directory of the project. 

    The file should be located at: `models/model.gguf`.

## Usage

1. **Prepare Data:**

    Ensure your data is formatted correctly and indexed in Elasticsearch. The `push_data_with_embeddings` function in `kb.py` handles indexing data with embeddings.

2. **Run the Application:**

    Execute the main script to start the chat system:

    ```bash
    python offlineChatwithLLM.py
    ```

    You will be prompted to enter queries, and the system will respond based on the indexed data and the LLaMA model.

## Configuration

- **LLaMA Model Path:** Update the `llm_model_path` variable in `kb.py` to the path of your quantized LLaMA model.
- **Elasticsearch Host:** Ensure the `es_host` variable points to your Elasticsearch instance.

## Additional Information

For more details on the LLaMA model used in this project, refer to the [LLaMA CPP Python GitHub Repository](https://github.com/abetlen/llama-cpp-python).

## Contributing

If you wish to contribute to this project, please fork the repository and create a pull request with your proposed changes.

## Contact

For any questions or issues, please contact [Muhammad-Anas-Azam-Bhatti](mailto:anas.azam40@gmail.com).
