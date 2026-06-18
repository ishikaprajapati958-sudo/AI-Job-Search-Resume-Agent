"""
Utility functions for standalone agent
"""

import re
import json
from typing import List, Dict, Any


def extract_json_from_text(text: str) -> Dict[str, Any]:
    """
    Extract JSON from text response

    Args:
        text: Text containing JSON

    Returns:
        Parsed JSON dictionary
    """
    try:
        # Try direct JSON parse
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to find JSON in text
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                return {"raw_text": text}
        return {"raw_text": text}


def parse_resume_text(resume_text: str) -> Dict[str, List[str]]:
    """
    Parse resume text into sections

    Args:
        resume_text: Raw resume text

    Returns:
        Dictionary with parsed sections
    """
    sections = {
        "contact": [],
        "summary": [],
        "experience": [],
        "education": [],
        "skills": [],
        "certifications": [],
    }

    current_section = "contact"
    lines = resume_text.split("\n")

    for line in lines:
        line_lower = line.lower().strip()

        if "summary" in line_lower or "objective" in line_lower:
            current_section = "summary"
        elif "experience" in line_lower or "employment" in line_lower:
            current_section = "experience"
        elif "education" in line_lower or "degree" in line_lower:
            current_section = "education"
        elif "skill" in line_lower:
            current_section = "skills"
        elif "certification" in line_lower or "credential" in line_lower:
            current_section = "certifications"

        if line.strip():
            sections[current_section].append(line.strip())

    return sections


def extract_keywords(text: str, keywords_list: List[str]) -> List[str]:
    """
    Extract matching keywords from text

    Args:
        text: Text to search
        keywords_list: List of keywords to match

    Returns:
        List of found keywords
    """
    found = []
    text_lower = text.lower()

    for keyword in keywords_list:
        if keyword.lower() in text_lower:
            found.append(keyword)

    return found


def calculate_skill_match_percentage(resume_skills: List[str], job_skills: List[str]) -> float:
    """
    Calculate skill match percentage between resume and job

    Args:
        resume_skills: Skills from resume
        job_skills: Required skills from job

    Returns:
        Match percentage (0-100)
    """
    if not job_skills:
        return 0.0

    resume_skills_lower = [s.lower() for s in resume_skills]
    matched = sum(1 for skill in job_skills if skill.lower() in resume_skills_lower)

    return (matched / len(job_skills)) * 100


def format_recommendations(recommendations: Dict[str, Any]) -> str:
    """
    Format recommendations for display

    Args:
        recommendations: Recommendations dictionary

    Returns:
        Formatted string
    """
    output = "📋 CAREER RECOMMENDATIONS\n"
    output += "=" * 50 + "\n\n"

    if "recommendations" in recommendations:
        output += recommendations["recommendations"]

    return output


def save_analysis_report(analysis: Dict[str, Any], filename: str = "analysis_report.json"):
    """
    Save analysis report to file

    Args:
        analysis: Analysis dictionary
        filename: Output filename
    """
    with open(filename, "w") as f:
        json.dump(analysis, f, indent=2)

    print(f"✅ Report saved to {filename}")


def load_resume_from_file(filepath: str) -> str:
    """
    Load resume from file

    Args:
        filepath: Path to resume file

    Returns:
        Resume text
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Resume file not found: {filepath}")
    except Exception as e:
        raise Exception(f"Error reading resume file: {str(e)}")
