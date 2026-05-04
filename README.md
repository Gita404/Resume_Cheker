# Resume Checker

A Streamlit-based tool that checks PDF resumes against a job description and gives a shortlisted / not-shortlisted verdict with detailed reasons.

Uses the **Hugging Face Inference API** (Mistral 7B Instruct) for AI-powered analysis. Falls back to keyword matching if the API key is not configured.

## How it works

1. Upload up to 10 PDF resumes.
2. Click **Analyze**.
3. Each resume is analyzed against the job description using an LLM (or keyword matching as fallback).
4. You get a clear **Shortlisted** or **Not Shortlisted** tag with plain-English reasons.

## Setup

```bash
cd backend
pip install -r requirements.txt
```

### Hugging Face API Key (optional but recommended)

1. Create a free account at [huggingface.co](https://huggingface.co).
2. Generate an API token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
3. Copy `backend/.env.example` to `backend/.env` and paste your key:

```bash
cp backend/.env.example backend/.env
```

Then edit `backend/.env`:
```
HF_API_KEY=hf_your_token_here
```

Without a key, the app still works using keyword matching.

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
  model.py            - Resume analysis (HF API + keyword fallback)
  job_description.py  - Job description and skill lists
  utils.py            - PDF text extraction and text processing
  requirements.txt    - Python dependencies
  .env.example        - Template for environment variables
```

## Changing the Job Description

Edit `backend/job_description.py` to change the company name, role, requirements, and skill lists.
