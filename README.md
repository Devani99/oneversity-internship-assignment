# oneversity-internship-assignment

# AI Microservices Internship Assignment

this is demo video link - https://drive.google.com/drive/folders/1aPHxmQ-_SE9tXVLmsLCUHOX5Mi4GUv6i?usp=sharing

## Features

1.  **Text Summarizer**: Condenses long text into a brief, easy-to-read summary.
2.  **Q&A over Documents**: Allows users to upload a PDF and ask questions directly related to its content.
3.  **Dynamic Learning Path Generator**: Creates a structured learning plan for any topic at a specified skill level.

## Tech Stack

-   **Backend**: Python, FastAPI, LangChain
-   **Frontend**: Streamlit
-   **LLM Provider**: OpenRouter (configured for Mistral-7B)
-   **Embeddings**: Hugging Face Sentence Transformers (local)
-   **Vector Store**: FAISS

## How to Run This Project

### Prerequisites

-   Python 3.10+
-   An OpenRouter API Key (free)

### 1. Backend Setup

First, set up and run the backend server.

# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install the required packages
pip install -r requirements.txt

# enter api key in llm_provider.py 
# OPENROUTER_API_KEY="enter api key here"

# Run the FastAPI server from the project's ROOT directory
cd ..
python -m uvicorn backend.main:app --reload
The backend API will be running at http://120.0.0.1:8000

### 2. Frontend Setup (for Bonus Points)
With the backend running, open a new terminal to start the frontend.

# Navigate to the frontend directory
cd frontend

# Install Streamlit and requests
pip install streamlit requests

# Run the Streamlit app
streamlit run app.py


