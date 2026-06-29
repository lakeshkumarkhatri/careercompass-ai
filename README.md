# CareerCompass AI

## Overview
CareerCompass AI is a tool to analyze resumes and match candidates with relevant job opportunities.

## API Documentation

### POST /api/analyze-resume
Analyzes an uploaded PDF resume and returns candidate details and skill insights.

### POST /api/match-jobs
Analyzes an uploaded PDF resume and returns ranked job matches based on skill overlap.

**Request:**
- `file`: PDF file containing the resume.

**Example Response:**
```json
{
  "candidate_name": "John Doe",
  "matches": [
    {
      "job": {
        "id": "1",
        "title": "Senior Software Engineer",
        "company": "Tech Corp",
        "skills": ["python", "fastapi", "docker", "kubernetes", "aws"]
      },
      "score": 40,
      "reason": "Matched 2 out of 5 required skills."
    }
  ]
}
```

## Setup & Running
1. `pip install -r requirements.txt`
2. Configure `.env` with `GOOGLE_API_KEY`.
3. `uvicorn app:app --reload`
4. Run tests: `pytest`
