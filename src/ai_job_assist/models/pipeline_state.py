from typing import Optional, TypedDict
from .profile import UserProfile


class PipelineState(TypedDict):
    """Shared state through the pipeline"""
    cv_raw: str
    #session_id: str  
    cv_parsed: dict  
    user_profile: Optional[UserProfile]  
    missing_fields: list
    clarifying_questions: list
    error: Optional[str]