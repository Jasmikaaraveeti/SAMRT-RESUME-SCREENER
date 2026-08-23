from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, index=True)
    description = Column(Text)
    required_skills = Column(String) # Comma-separated
    minimum_experience = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    screening_results = relationship("ScreeningResult", back_populates="job")

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String)
    location = Column(String)
    experience = Column(Float)
    education = Column(String)
    extracted_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    skills = relationship("Skill", back_populates="candidate")
    screening_results = relationship("ScreeningResult", back_populates="candidate", cascade="all, delete-orphan")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    skill_name = Column(String, index=True)
    skill_level = Column(String) # e.g., Beginner, Intermediate, Expert

    candidate = relationship("Candidate", back_populates="skills")

class ScreeningResult(Base):
    __tablename__ = "screening_results"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    match_score = Column(Float)
    skills_score = Column(Float)
    experience_score = Column(Float)
    education_score = Column(Float)
    matched_skills = Column(String)
    missing_skills = Column(String)
    justification = Column(Text)
    strengths = Column(Text)
    weaknesses = Column(Text)
    recommendation = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    candidate = relationship("Candidate", back_populates="screening_results")
    job = relationship("Job", back_populates="screening_results")
