# CareerCompass AI - Sprint 0

## Overview
Initial setup of CareerCompass AI using FastAPI.

## Installation
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Server
```bash
uvicorn app:app --reload
```

## Project Structure
- `api/`: API endpoints
- `core/`: Core utilities and configuration
- `tests/`: Test suite
