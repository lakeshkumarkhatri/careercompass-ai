import json
import logging
from pathlib import Path
from typing import List
from models.job import Job
from models.job_match import JobMatch

logger = logging.getLogger(__name__)

def load_jobs() -> List[Job]:
    """Load jobs from JSON file."""
    data_path = Path("data/jobs.json")
    if not data_path.exists():
        logger.error(f"Jobs file not found at {data_path}")
        raise FileNotFoundError(f"Jobs file not found at {data_path}")
    
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Job(**item) for item in data]
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode jobs JSON: {e}")
        raise ValueError("Invalid format in jobs data")

def calculate_match_score(resume_skills: List[str], job_skills: List[str]) -> tuple[int, str]:
    """Calculate match score and reason."""
    if not job_skills:
        return 0, "No skills required for this job."
    
    resume_skills_lower = {skill.lower() for skill in resume_skills}
    job_skills_lower = {skill.lower() for skill in job_skills}
    
    intersection = resume_skills_lower.intersection(job_skills_lower)
    score = int((len(intersection) / len(job_skills_lower)) * 100)
    
    reason = f"Matched {len(intersection)} out of {len(job_skills_lower)} required skills."
    
    return score, reason

def get_top_matches(resume_skills: List[str], top_n: int = 5) -> List[JobMatch]:
    """Return top N job matches based on skill overlap."""
    jobs = load_jobs()
    matches = []
    
    for job in jobs:
        score, reason = calculate_match_score(resume_skills, job.skills)
        matches.append(JobMatch(job=job, score=score, reason=reason))
    
    # Sort by score descending
    matches.sort(key=lambda x: x.score, reverse=True)
    
    return matches[:top_n]
