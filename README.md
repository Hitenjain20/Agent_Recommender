# Agent_Recommender

This repository contains the code for a custom query engine using the `llama_index` library and a Streamlit app for interacting with the engine. The chatbot helps users choose a Language Model (LLM) for their use case.

## Files

- `inference.py`: Contains the code for the custom query engine.
- `app.py`: Contains the Streamlit app code for interacting with the query engine.
- `api.py`: Contains fastapi code for interacting with the query engine
- `custome_retriever.py`: Contains the code for custom retriever including keyword and vector search

## Setup

### Prerequisites

- Python 3.7 or higher
- Streamlit
- Required Python packages (listed in `requirements.txt`)

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/llm-selection-chatbot.git
    cd llm-selection-chatbot
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your API key:

    ```env
    GOOGLE_API_KEY=your_google_api_key
    ```

## Running the App

1. Ensure you have the `inference.py` and `app.py` files in the same directory.

2. Run the Streamlit app:

    ```sh
    streamlit run app.py
    ```

3. Open your web browser and go to `http://localhost:8000` to interact with the chatbot.

## Code Overview

### `inference.py`

This file contains the `Inference` class, which initializes the LLM and embedding models, loads documents, and processes queries using a custom retriever.

### `app.py`

This file contains the Streamlit app code. It sets up the chatbot interface, handles user input, and displays responses from the custom query engine.

### Example Usage

1. Start the Streamlit app.
2. Enter your query in the input box.
3. The chatbot will respond with the best-fit agent based on your query.

