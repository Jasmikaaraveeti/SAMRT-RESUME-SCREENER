from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn
import random

from database import get_db, Base, engine
import models
import schemas
from mock_ai_service import generate_mock_screening_result
from pdf_service import extract_text_from_pdf, parse_resume_text

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Resume Screener API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/jobs", response_model=schemas.Job)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    db_job = models.Job(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.get("/api/jobs", response_model=List[schemas.Job])
def get_jobs(db: Session = Depends(get_db)):
    return db.query(models.Job).all()

@app.post("/api/resumes/upload")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    if file.filename.endswith('.pdf'):
        text = extract_text_from_pdf(contents)
    else:
        text = contents.decode('utf-8', errors='ignore')
        
    parsed_data = parse_resume_text(text)
    
    db_candidate = models.Candidate(**parsed_data)
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    
    mock_skills = ["Java", "SQL", "Python", "React", "Spring Boot", "REST API", "Git", "Docker", "AWS"]
    selected_skills = random.sample(mock_skills, k=random.randint(3, 6))
    
    for skill_name in selected_skills:
        db_skill = models.Skill(candidate_id=db_candidate.id, skill_name=skill_name, skill_level="Intermediate")
        db.add(db_skill)
    
    db.commit()
    db.refresh(db_candidate)
    
    return db_candidate

@app.post("/api/screen")
def screen_candidates(req: schemas.ScreenRequest, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == req.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    results = []
    for c_id in req.candidate_ids:
        candidate = db.query(models.Candidate).filter(models.Candidate.id == c_id).first()
        if not candidate:
            continue
            
        ai_result = generate_mock_screening_result(
            candidate.extracted_text, 
            job.description, 
            job.required_skills
        )
        
        db_result = models.ScreeningResult(
            candidate_id=candidate.id,
            job_id=job.id,
            **ai_result
        )
        db.add(db_result)
        db.commit()
        db.refresh(db_result)
        results.append(db_result)
        
    return results

@app.get("/api/candidates", response_model=List[schemas.Candidate])
def get_candidates(db: Session = Depends(get_db)):
    return db.query(models.Candidate).all()

@app.get("/api/candidates/{candidate_id}")
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    results = db.query(models.ScreeningResult).filter(models.ScreeningResult.candidate_id == candidate_id).all()
    
    return {
        "candidate": candidate,
        "screening_results": results
    }
    
@app.get("/api/screening-results", response_model=List[schemas.ScreeningResult])
def get_screening_results(job_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.ScreeningResult)
    if job_id:
        query = query.filter(models.ScreeningResult.job_id == job_id)
    return query.all()

@app.get("/api/analytics")
def get_analytics(db: Session = Depends(get_db)):
    total_resumes = db.query(models.Candidate).count()
    results = db.query(models.ScreeningResult).all()
    
    if not results:
        return {
            "total_resumes": total_resumes,
            "shortlisted": 0,
            "average_score": 0,
            "jobs_analyzed": db.query(models.Job).count()
        }
        
    shortlisted = sum(1 for r in results if r.recommendation in ["Shortlist", "Shortlist for Technical Interview"])
    avg_score = sum(r.match_score for r in results) / len(results)
    
    return {
        "total_resumes": total_resumes,
        "shortlisted": shortlisted,
        "average_score": round(avg_score, 1),
        "jobs_analyzed": db.query(models.Job).count()
    }

@app.post("/api/demo-data")
def load_demo_data(db: Session = Depends(get_db)):
    job = models.Job(
        job_title="Software Engineer",
        description="Looking for a Software Engineer with Java, SQL, Spring Boot, REST API, and problem-solving experience.",
        required_skills="Java, SQL, Spring Boot, REST API, Git",
        minimum_experience=2.0
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    
    demo_candidates = [
        {"name": "Rahul Sharma", "email": "rahul.s@example.com", "phone": "+91 9876543210", "location": "Bangalore", "experience": 3.5, "education": "B.Tech Computer Science"},
        {"name": "Priya Reddy", "email": "priya.r@example.com", "phone": "+91 8765432109", "location": "Hyderabad", "experience": 2.8, "education": "M.Tech Software Engineering"},
    ]
    
    skills_map = {
        "Rahul Sharma": ["Java", "SQL", "Spring Boot", "REST API", "Git"],
        "Priya Reddy": ["Java", "SQL", "Spring Boot", "React", "Git"],
    }
    
    for c in demo_candidates:
        cand = models.Candidate(**c, extracted_text=f"Demo resume for {c['name']}")
        db.add(cand)
        db.commit()
        db.refresh(cand)
        
        for skill in skills_map[c['name']]:
            db_skill = models.Skill(candidate_id=cand.id, skill_name=skill, skill_level="Intermediate")
            db.add(db_skill)
            
        ai_result = generate_mock_screening_result(cand.extracted_text, job.description, job.required_skills)
        res = models.ScreeningResult(candidate_id=cand.id, job_id=job.id, **ai_result)
        db.add(res)
        
    db.commit()
    return {"message": "Demo data loaded successfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
