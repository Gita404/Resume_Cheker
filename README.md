# Resume Checker

A Streamlit app that analyzes PDF resumes against a job description and returns a **Shortlisted / Not Shortlisted** verdict with plain-English reasons.

Powered by the **Hugging Face Inference API** (Mistral 7B Instruct). Falls back to keyword matching if no API key is set.

---

## Setup

```bash
cd Website
pip install -r requirements.txt
```

**API Key (optional but recommended)**

```bash
cp .env.example .env
```

Edit `.env`:
```
HF_API_KEY=hf_your_token_here
```

Get a free token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).  
Without a key, the app falls back to keyword matching.

---

## Run

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`.

---

## Usage

1. Select a job description from the list.
2. Upload up to 5 PDF resumes.
3. Click **Analyze**.

---


## Adding Job Descriptions

Edit `job_description.py` — add entries to `JOB_LISTINGS` with a title, company, description, required skills, and bonus skills.



## Results

<img width="1868" height="718" alt="image" src="https://github.com/user-attachments/assets/cec84e5b-1d46-490f-8bcb-f785b10d8efb" />

<img width="1864" height="756" alt="image" src="https://github.com/user-attachments/assets/3b67ed3c-8c9c-4c64-8add-909da2ce9773" />


