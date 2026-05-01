"""
Resume analysis logic.

Uses keyword matching against the job description to determine
whether a candidate should be shortlisted. No external API needed.
"""

import re
from utils import extract_skills_from_text, clean_text
from job_description import (
    JOB_DESCRIPTION, JOB_TITLE, COMPANY_NAME,
    REQUIRED_SKILLS, BONUS_SKILLS,
    MINIMUM_REQUIRED_MATCH_PERCENT,
)


def _deduplicate_skills(skills: list) -> list:
    """Collapse known synonyms so the output reads cleanly."""
    synonyms = {
        "nodejs": "Node.js",
        "node.js": "Node.js",
        "reactjs": "React",
        "react.js": "React",
        "react": "React",
        "fullstack": "Full Stack",
        "full-stack": "Full Stack",
        "full stack": "Full Stack",
        "restful": "REST",
        "rest": "REST",
        "nosql": "NoSQL",
        "postgresql": "PostgreSQL",
        "mysql": "MySQL",
        "mongodb": "MongoDB",
        "vuejs": "Vue",
        "nextjs": "Next.js",
        "cicd": "CI/CD",
        "ci/cd": "CI/CD",
        "github actions": "GitHub Actions",
        "ec2": "EC2",
        "s3": "S3",
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


def analyze_resume(resume_text: str) -> dict:
    """
    Analyze a resume against the hardcoded job description.

    Returns a dict with:
        - is_shortlisted (bool)
        - reasons (list of plain-English strings)
        - matched / missing skill lists
    """
    cleaned = clean_text(resume_text)

    matched_required_raw = extract_skills_from_text(cleaned, REQUIRED_SKILLS)
    matched_bonus_raw = extract_skills_from_text(cleaned, BONUS_SKILLS)

    missing_required_raw = [
        s for s in REQUIRED_SKILLS
        if s.lower() not in [m.lower() for m in matched_required_raw]
    ]

    # De-duplicate for display
    matched_required = _deduplicate_skills(matched_required_raw)
    matched_bonus = _deduplicate_skills(matched_bonus_raw)
    missing_required = _deduplicate_skills(missing_required_raw)

    total_required = len(set(s.lower() for s in REQUIRED_SKILLS))
    matched_count = len(matched_required)
    match_pct = round((len(matched_required_raw) / len(REQUIRED_SKILLS)) * 100, 1) if REQUIRED_SKILLS else 0

    is_shortlisted = match_pct >= MINIMUM_REQUIRED_MATCH_PERCENT

    # --- Build straight-to-point reasons ---
    reasons = []

    if is_shortlisted:
        reasons.append(
            f"Meets the minimum skill requirement for {JOB_TITLE} at {COMPANY_NAME}."
        )
        if matched_required:
            reasons.append(
                f"Required skills found: {', '.join(matched_required)}."
            )
        if matched_bonus:
            reasons.append(
                f"Also has good-to-have skills: {', '.join(matched_bonus)}."
            )
        if missing_required:
            reasons.append(
                f"Missing but can be picked up: {', '.join(missing_required)}."
            )
    else:
        reasons.append(
            f"Does not meet the minimum skill requirement for {JOB_TITLE} at {COMPANY_NAME}."
        )
        if missing_required:
            reasons.append(
                f"Key skills missing: {', '.join(missing_required)}."
            )
        if matched_required:
            reasons.append(
                f"Skills that did match: {', '.join(matched_required)}."
            )
        if matched_bonus:
            reasons.append(
                f"Has some good-to-have skills: {', '.join(matched_bonus)}."
            )
        if not matched_required:
            reasons.append(
                "Resume does not appear to mention any of the required technologies."
            )

    return {
        "is_shortlisted": is_shortlisted,
        "reasons": reasons,
    }
