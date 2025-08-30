from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from ..llm_provider import get_llm

router = APIRouter()

class LearningPathRequest(BaseModel):
    topic: str
    level: str

@router.post("/generate-learning-path")
async def generate_learning_path(request: LearningPathRequest):
    try:
        llm = get_llm()
        prompt_template = """
        You are an expert curriculum designer. Create a structured, step-by-step learning path for someone who wants to learn '{topic}' at a '{level}' level.

        The path should include core concepts, key skills, project ideas, and recommended resource types. Format the output clearly in Markdown.

        LEARNING PATH:
        """
        prompt = PromptTemplate(input_variables=["topic", "level"], template=prompt_template)
        chain = LLMChain(llm=llm, prompt=prompt)
        
        path = chain.invoke({"topic": request.topic, "level": request.level})
        return {"learning_path": path['text']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))