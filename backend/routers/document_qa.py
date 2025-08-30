import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.chains.retrieval_qa.base import RetrievalQA
from ..llm_provider import get_llm, get_embeddings

router = APIRouter()


DOCS_DIR = "docs/"
VECTOR_STORE_PATH = "vector_store/faiss_index"

class AskRequest(BaseModel):
    query: str

@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
        
    file_path = os.path.join(DOCS_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
        
    try:
        loader = PyPDFLoader(file_path)
        docs = loader.load_and_split()
        
        embeddings = get_embeddings()

        db = FAISS.from_documents(docs, embeddings)
        db.save_local(VECTOR_STORE_PATH)
        
        return {"message": f"Document '{file.filename}' processed successfully."}
    except Exception as e:
        print(f"An error occurred during document processing: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")


@router.post("/ask-document")
async def ask_document(request: AskRequest):
    if not os.path.exists(VECTOR_STORE_PATH):
        raise HTTPException(status_code=400, detail="No document has been processed. Please upload a document first.")
            
    try:
        llm = get_llm()
        embeddings = get_embeddings()
        
        vector_store = FAISS.load_local(
            VECTOR_STORE_PATH, 
            embeddings=embeddings, 
            allow_dangerous_deserialization=True
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever()
        )
        result = qa_chain.invoke({"query": request.query})
        return {"answer": result['result']}
    except Exception as e:
        print(f"An error occurred during Q&A: {e}")
        raise HTTPException(status_code=500, detail=str(e))