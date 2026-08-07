from pydantic import BaseModel
from typing import List, Optional

class PersonalInfo(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None

class Education(BaseModel):
    degree: str
    institution: str
    graduation_year: int
    gpa: Optional[float] = None
    relevant_coursework: Optional[List[str]] = None

class WorkExperience(BaseModel):
    title: str
    company: str
    start_date: str
    end_date: Optional[str] = None
    description: str
    technologies: List[str]

class Skills(BaseModel):
    hard_skills: dict
    soft_skills: dict

class Project(BaseModel):
    name: str
    description: str
    technologies: List[str]
    url: Optional[str] = None

class UserProfile(BaseModel):
    personal_info: PersonalInfo
    education: List[Education]
    work_experience: List[WorkExperience]
    skills: Skills
    projects: Optional[List[Project]] = None
    certifications: Optional[List[str]] = None
    languages: Optional[List[str]] = None