from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..llm_provider import get_llm

router = APIRouter()

class SummarizeRequest(BaseModel):
    text: str

@router.post("/summarize")
async def summarize_text(request: SummarizeRequest):
    try:
        llm = get_llm()

    
        prompt = f"Provide a concise summary of the following text:\n\n{request.text}\n\nSUMMARY:"
        result = llm.invoke(prompt)


        if hasattr(result, "content"):
            summary = result.content
        elif isinstance(result, dict) and "text" in result:
            summary = result["text"]
        else:
            summary = str(result)

        return {"summary": summary.strip()}

    except Exception as e:
        print(f"Summarization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
