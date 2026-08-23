from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class JobBase(BaseModel):
    job_title: str
    description: str
    required_skills: str
    minimum_experience: float

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class SkillBase(BaseModel):
    skill_name: str
    skill_level: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class Skill(SkillBase):
    id: int
    class Config:
        from_attributes = True

class CandidateBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    experience: float
    education: Optional[str] = None
    extracted_text: Optional[str] = None

class CandidateCreate(CandidateBase):
    pass

class Candidate(CandidateBase):
    id: int
    created_at: datetime
    skills: List[Skill] = []
    class Config:
        from_attributes = True

class ScreenRequest(BaseModel):
    job_id: int
    candidate_ids: List[int]

class ScreeningResultBase(BaseModel):
    match_score: float
    skills_score: float
    experience_score: float
    education_score: float
    matched_skills: str
    missing_skills: str
    justification: str
    strengths: str
    weaknesses: str
    recommendation: str

class ScreeningResultCreate(ScreeningResultBase):
    pass

class ScreeningResult(ScreeningResultBase):
    id: int
    created_at: datetime
    candidate: Candidate
    job: Job
    class Config:
        from_attributes = True
