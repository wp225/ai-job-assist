from fastapi import APIRouter
from ..models.schemas import AnalyzeRequest, AnalyzeResponse
from fastapi import File, UploadFile, HTTPException
import os
import shutil
from ..agents.pipeline import cv_parsing_graph
from ..models.pipeline_state import PipelineState
from pypdf import PdfReader
from io import BytesIO

UPLOAD_PATH = "resume"
router = APIRouter()

@router.post("/analyze")
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    #TODO: Call CLaude
    return AnalyzeResponse(
        fit_score=75,
        summary="Testing Response"
    )


@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        # Extract PDF text
        pdf_content = await file.read()
        pdf_reader = PdfReader(BytesIO(pdf_content))
        cv_raw = "\n".join([page.extract_text() for page in pdf_reader.pages])
        
        # Create initial state
        initial_state = {
            "cv_raw": cv_raw,
            "cv_parsed": {},
            "user_profile": None,
            "missing_fields": [],
            "clarifying_questions": [],
            "error": None
        }
        
        # Invoke graph
        result = cv_parsing_graph.invoke(initial_state)
        
        # Return results
        return {
            "status": "success",
            "cv_parsed": result.get("cv_parsed"),
            "missing_fields": result.get("missing_fields"),
            "error": result.get("error")
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
    