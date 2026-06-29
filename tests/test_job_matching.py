import pytest
from services.job_matching_service import calculate_match_score, get_top_matches
from models.job import Job

def test_score_calculation():
    resume_skills = ["python", "fastapi"]
    job_skills = ["python", "fastapi", "docker"]
    score, reason = calculate_match_score(resume_skills, job_skills)
    assert score == 66  # (2/3)*100 = 66.66 -> 66
    assert "Matched 2 out of 3 required skills." in reason

def test_empty_skills():
    resume_skills = []
    job_skills = ["python"]
    score, reason = calculate_match_score(resume_skills, job_skills)
    assert score == 0
    assert "Matched 0 out of 1 required skills." in reason

def test_empty_jobs_skills():
    resume_skills = ["python"]
    job_skills = []
    score, reason = calculate_match_score(resume_skills, job_skills)
    assert score == 0
    assert "No skills required" in reason

def test_sorting_and_limit():
    # This relies on the jobs.json file which has 5 jobs.
    # It should return top 5 (which is all of them if <= 5)
    resume_skills = ["python"]
    matches = get_top_matches(resume_skills, top_n=2)
    
    assert len(matches) == 2
    # Verify sorting: higher scores first
    assert matches[0].score >= matches[1].score
