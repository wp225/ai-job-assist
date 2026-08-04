from fastapi import APIRouter
from ..models.schemas import AnalyzeRequest, AnalyzeResponse

router = APIRouter()

@router.post("/analyze")
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    #TODO: Call CLaude
    return AnalyzeResponse(
        fit_score=75,
        summary="Testing Response"
    )
