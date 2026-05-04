"""
Resume analysis logic.

Uses Hugging Face Inference API (a small LLM) to analyze resumes
against a job description. Falls back to keyword matching if the
API is unavailable or the key is not set.
"""

import os
import re
import json
import requests
from dotenv import load_dotenv
from utils import extract_skills_from_text, clean_text

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY", "")
HF_MODEL = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"


# -- Hugging Face LLM Analysis ------------------------------------------------

def _build_prompt(resume_text: str, jd: dict) -> str:
    """Build the prompt sent to the LLM."""
    resume_excerpt = resume_text[:3000]

    return f"""You are an experienced HR recruiter. Analyze the following resume against the given job description and decide if the candidate should be shortlisted.

Job Description:
{jd['description'].strip()}

Resume:
{resume_excerpt}

Respond in valid JSON only, nothing else. Use this exact format:
{{"is_shortlisted": true or false, "reasons": ["reason 1", "reason 2", "reason 3"]}}

Rules for your analysis:
- Give 3 to 5 short, specific reasons.
- Each reason should be one clear sentence.
- Do not use emojis or exclamation marks.
- Be direct and factual, like a human recruiter would be.
- If shortlisted, mention what skills matched and any gaps.
- If not shortlisted, mention what critical skills are missing.

JSON:"""


def _call_huggingface(resume_text: str, jd: dict) -> dict | None:
    """
    Call the Hugging Face Inference API.
    Returns parsed result dict or None on failure.
    """
    if not HF_API_KEY:
        return None

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json",
    }

    prompt = _build_prompt(resume_text, jd)

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 400,
            "temperature": 0.3,
            "return_full_text": False,
        },
    }

    try:
        resp = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        if isinstance(data, list) and len(data) > 0:
            generated = data[0].get("generated_text", "")
        elif isinstance(data, dict):
            generated = data.get("generated_text", "")
        else:
            return None

        json_match = re.search(r'\{.*\}', generated, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            if "is_shortlisted" in result and "reasons" in result:
                result["is_shortlisted"] = bool(result["is_shortlisted"])
                result["reasons"] = [str(r) for r in result["reasons"]][:6]
                return result

    except (requests.RequestException, json.JSONDecodeError, KeyError, ValueError):
        pass

    return None


# -- Keyword Fallback ----------------------------------------------------------

def _deduplicate_skills(skills: list) -> list:
    """Collapse known synonyms so the output reads cleanly."""
    synonyms = {
        "nodejs": "Node.js", "node.js": "Node.js",
        "reactjs": "React", "react.js": "React", "react": "React",
        "fullstack": "Full Stack", "full-stack": "Full Stack", "full stack": "Full Stack",
        "restful": "REST", "rest": "REST",
        "nosql": "NoSQL",
        "postgresql": "PostgreSQL", "mysql": "MySQL", "mongodb": "MongoDB",
        "vuejs": "Vue", "nextjs": "Next.js",
        "cicd": "CI/CD", "ci/cd": "CI/CD",
        "github actions": "GitHub Actions",
        "ec2": "EC2", "s3": "S3", "ecs": "ECS", "rds": "RDS",
        "powerbi": "Power BI", "power bi": "Power BI",
        "k8s": "Kubernetes", "kubernetes": "Kubernetes",
    }
    seen = set()
    cleaned = []
    for skill in skills:
        normalized = synonyms.get(skill.lower(), skill)
        key = normalized.lower()
        if key not in seen:
            seen.add(key)
            cleaned.append(normalized)
    return sorted(cleaned)


def _keyword_fallback(resume_text: str, jd: dict) -> dict:
    """Pure keyword matching fallback when the LLM is unavailable."""
    cleaned = clean_text(resume_text)

    required = jd.get("required_skills", [])
    bonus = jd.get("bonus_skills", [])
    min_pct = jd.get("min_match_percent", 25)

    matched_required_raw = extract_skills_from_text(cleaned, required)
    matched_bonus_raw = extract_skills_from_text(cleaned, bonus)

    missing_required_raw = [
        s for s in required
        if s.lower() not in [m.lower() for m in matched_required_raw]
    ]

    matched_required = _deduplicate_skills(matched_required_raw)
    matched_bonus = _deduplicate_skills(matched_bonus_raw)
    missing_required = _deduplicate_skills(missing_required_raw)

    match_pct = round(
        (len(matched_required_raw) / len(required)) * 100, 1
    ) if required else 0

    is_shortlisted = match_pct >= min_pct
    title = jd.get("title", "this role")

    reasons = []

    if is_shortlisted:
        reasons.append(f"Meets the minimum skill threshold for {title}.")
        if matched_required:
            reasons.append(f"Required skills found: {', '.join(matched_required)}.")
        if matched_bonus:
            reasons.append(f"Also has good-to-have skills: {', '.join(matched_bonus)}.")
        if missing_required:
            reasons.append(f"Missing but can be picked up: {', '.join(missing_required)}.")
    else:
        reasons.append(f"Does not meet the minimum skill threshold for {title}.")
        if missing_required:
            reasons.append(f"Key skills not found: {', '.join(missing_required)}.")
        if matched_required:
            reasons.append(f"Skills that did match: {', '.join(matched_required)}.")
        if matched_bonus:
            reasons.append(f"Has some good-to-have skills: {', '.join(matched_bonus)}.")
        if not matched_required:
            reasons.append("Resume does not appear to mention any of the required technologies.")

    return {
        "is_shortlisted": is_shortlisted,
        "reasons": reasons,
    }


# -- Public API ----------------------------------------------------------------

def analyze_resume(resume_text: str, jd: dict) -> dict:
    """
    Analyze a resume against a job description.

    Tries the Hugging Face LLM first, falls back to keyword matching.

    Args:
        resume_text: extracted text from the PDF
        jd: a single job listing dict from JOB_LISTINGS

    Returns:
        dict with is_shortlisted (bool) and reasons (list of str)
    """
    llm_result = _call_huggingface(resume_text, jd)
    if llm_result:
        return llm_result

    return _keyword_fallback(resume_text, jd)
