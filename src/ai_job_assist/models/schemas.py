from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    cv_text: str
    job_posting: str
    
class AnalyzeResponse(BaseModel):
    fit_score: float = Field(le = 100, ge = 0)
    summary: str
    
