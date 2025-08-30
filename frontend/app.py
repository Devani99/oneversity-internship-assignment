import streamlit as st
import requests
import time

# --- CONFIGURATION ---
st.set_page_config(
    page_title="AI Microservices Demo",
    page_icon="🤖",
    layout="wide"
)

# Define the base URL for the FastAPI backend
BACKEND_URL = "http://127.0.0.1:8000/api"

# --- HELPER FUNCTIONS ---
def call_api(endpoint, json_data=None, files=None, timeout=30):
    """Helper function to call the backend API with timeout."""
    url = f"{BACKEND_URL}/{endpoint}"
    try:
        if files:
            response = requests.post(url, files=files, timeout=timeout)
        else:
            response = requests.post(url, json=json_data, timeout=timeout)
        
        response.raise_for_status()
        data = response.json()
        if not data:
            st.error("Empty response from server")
            return None
        return data
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        if status_code == 400:
            st.error(f"Bad request: {e.response.text}")
        elif status_code == 500:
            st.error(f"Server error: {e.response.text}")
        else:
            st.error(f"API call failed: {e.response.text}")
        return None
    except requests.exceptions.Timeout:
        st.error(f"Request timed out after {timeout} seconds")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"API call failed: {str(e)}")
        return None

# --- UI LAYOUT ---
st.title("Internship Assignment: AI Microservices 🚀")
st.markdown(
    """
    Welcome to an interactive demo of AI microservices built with **FastAPI**, **LangChain**, and **Streamlit**. 
    Powered by **Mistral-7B** via **OpenRouter** and **HuggingFace embeddings**, this app offers:
    - **Text Summarization**: Condense long text into concise summaries.
    - **Q&A over Documents**: Upload a PDF and ask questions about its content.
    - **Learning Path Generator**: Get a personalized learning plan for any topic.
    """
)

# Initialize session state
if 'document_ready' not in st.session_state:
    st.session_state['document_ready'] = False
if 'uploaded_file_name' not in st.session_state:
    st.session_state['uploaded_file_name'] = None

# Create tabs for each microservice
tab1, tab2, tab3 = st.tabs(["**1. Text Summarizer**", "**2. Q&A over Documents**", "**3. Learning Path Generator**"])

with tab1:
    st.header("📝 Text Summarization")
    st.write("Paste any text to get a concise summary powered by Mistral-7B.")
    
    input_text = st.text_area("Enter Text Here:", height=250, placeholder="Paste your article, report, or any long text...")
    
    if st.button("✨ Generate Summary", key="summarize"):
        if input_text:
            with st.spinner("Summarizing... Please wait."):
                payload = {"text": input_text}
                result = call_api("summarize", json_data=payload)
                if result and "summary" in result:
                    st.success("Summary Generated!")
                    st.markdown(f"> **Summary**: {result['summary']}")
                else:
                    st.error("Failed to generate summary. Check backend logs.")
        else:
            st.warning("Please enter some text to summarize.")

with tab2:
    st.header("❓ Q&A Over Your Documents")
    st.write("Upload a PDF document and ask questions about its content using vector search.")
    
    uploaded_file = st.file_uploader("Upload a PDF document", type="pdf", key="file_uploader")
    
    if uploaded_file is not None:
        # Reset document state when a new file is uploaded
        if st.session_state['uploaded_file_name'] != uploaded_file.name:
            st.session_state['document_ready'] = False
            st.session_state['uploaded_file_name'] = uploaded_file.name
        
        with st.spinner(f"Processing {uploaded_file.name}... This may take a moment."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            result = call_api("upload-document", files=files)
            if result and "message" in result:
                st.success(result["message"])
                st.session_state['document_ready'] = True
            else:
                st.error("Failed to process document. Check backend logs.")
    
    if st.session_state.get('document_ready', False):
        st.write("---")
        st.write(f"Document '{st.session_state['uploaded_file_name']}' ready! Ask your question.")
        query = st.text_input("Ask a question about the document:", key="query_input")
        
        if st.button("💬 Get Answer", key="ask"):
            if query:
                with st.spinner("Searching for the answer..."):
                    payload = {"query": query}
                    result = call_api("ask-document", json_data=payload)
                    if result and "answer" in result:
                        st.info("Answer:")
                        st.markdown(result['answer'])
                    else:
                        st.error("Failed to retrieve answer. Check backend logs.")
            else:
                st.warning("Please enter a question.")
    else:
        st.info("Please upload a document to begin.")

with tab3:
    st.header("🗺️ Dynamic Learning Path Generator")
    st.write("Enter a topic and your skill level to get a personalized learning path.")
    
    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("Topic:", placeholder="e.g., 'Machine Learning', 'Quantum Computing'")
    with col2:
        level = st.selectbox("Skill Level:", ["Beginner", "Intermediate", "Advanced"])
        
    if st.button("🧠 Generate Path", key="learning_path"):
        if topic:
            with st.spinner(f"Crafting a {level} learning path for {topic}..."):
                payload = {"topic": topic, "level": level}
                result = call_api("generate-learning-path", json_data=payload)
                if result and "learning_path" in result:
                    st.success("Learning Path Generated!")
                    st.markdown("### Learning Path")
                    # Format learning path as a numbered list
                    steps = result['learning_path'].split("\n")
                    for i, step in enumerate(steps, 1):
                        if step.strip():
                            st.markdown(f"{i}. {step.strip()}")
                else:
                    st.error("Failed to generate learning path. Check backend logs.")
        else:
            st.warning("Please enter a topic.")