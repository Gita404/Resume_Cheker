# Resume Checker

A Streamlit-based tool that checks PDF resumes against a hardcoded job description and gives a straight-to-point shortlisted / not-shortlisted verdict with reasons.

## How it works

1. Upload up to 5 PDF resumes.
2. Click **Analyze**.
3. Each resume is checked against the job description (keyword/skill matching).
4. You get a clear **Shortlisted** or **Not Shortlisted** tag with plain-English reasons.

No external APIs needed. Everything runs locally.

## Setup

```bash
cd backend
pip install -r requirements.txt
```

## Run

```bash
cd backend
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Project Structure

```
backend/
  app.py              - Streamlit UI
  model.py            - Resume analysis logic
  job_description.py  - Hardcoded job description and skill lists
  utils.py            - PDF text extraction and text processing
  requirements.txt    - Python dependencies
frontend/
  index.html          - (static frontend, not used by the checker)
  style.css
  script.js
```

## Changing the Job Description

Edit `backend/job_description.py` to change the company name, role, requirements, and skill lists.
