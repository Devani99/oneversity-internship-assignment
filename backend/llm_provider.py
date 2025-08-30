from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings


MY_API_KEY = "enter your api key"

def get_llm():
    """
    Initializes the LLM using the official ChatOpenAI client,
    configured to point to OpenRouter's API.
    """
    return ChatOpenAI(
        model="mistralai/mistral-7b-instruct",
        api_key=MY_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "Internship App"
        }
    )


def get_embeddings():
    """
    Initializes and returns a local HuggingFace embedding model.
    This is reliable and removes dependency on a network call for embeddings.
    """

    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    
    print(f"Using HuggingFaceEmbeddings with model: {model_name}")
    
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )