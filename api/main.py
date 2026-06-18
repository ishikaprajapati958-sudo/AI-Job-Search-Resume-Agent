"""
FastAPI REST API for Job Search Agent
Provides endpoints for all agent functionality
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from standalone_agent.agent import JobSearchAgent
from loguru import logger

app = FastAPI(
    title="Job Search & Resume Agent API",
    description="Multi-agent system for job search and resume improvement",
    version="1.0.0",
)

# Initialize agent
agent = JobSearchAgent()

logger.add("logs/api.log")


# Pydantic Models
class ResumeAnalysisRequest(BaseModel):
    resume_text: str


class SkillExtractionRequest(BaseModel):
    resume_text: str


class JobSearchRequest(BaseModel):
    skills: List[str]
    location: str = "Remote"
    experience_level: str = "Mid"


class JobMatchingRequest(BaseModel):
    resume_text: str
    job_description: str


class RecommendationsRequest(BaseModel):
    resume_text: str
    target_role: str
    industry: str = "Technology"


class InterviewQuestionsRequest(BaseModel):
    job_title: str
    skills: List[str]


class MarketInsightsRequest(BaseModel):
    skills: List[str]
    industry: str = "Technology"


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "agent": "ready"}


@app.post("/api/analyze-resume")
async def analyze_resume(request: ResumeAnalysisRequest):
    """
    Analyze a resume for quality, structure, and effectiveness

    Args:
        request: Resume analysis request with resume text

    Returns:
        Analysis results
    """
    try:
        logger.info("Resume analysis request received")
        result = agent.analyze_resume(request.resume_text)
        return result
    except Exception as e:
        logger.error(f"Error in resume analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/extract-skills")
async def extract_skills(request: SkillExtractionRequest):
    """
    Extract skills from resume

    Args:
        request: Skill extraction request

    Returns:
        Extracted skills categorized by type
    """
    try:
        logger.info("Skill extraction request received")
        result = agent.extract_skills(request.resume_text)
        return result
    except Exception as e:
        logger.error(f"Error in skill extraction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search-jobs")
async def search_jobs(request: JobSearchRequest):
    """
    Search for relevant job opportunities

    Args:
        request: Job search request with skills and preferences

    Returns:
        List of relevant job opportunities
    """
    try:
        logger.info(f"Job search request received for skills: {request.skills}")
        result = agent.search_jobs(request.skills, request.location, request.experience_level)
        return result
    except Exception as e:
        logger.error(f"Error in job search: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/match-jobs")
async def match_jobs(request: JobMatchingRequest):
    """
    Match resume against job description

    Args:
        request: Job matching request

    Returns:
        Match analysis with score and gap analysis
    """
    try:
        logger.info("Job matching request received")
        result = agent.match_resume_to_job(request.resume_text, request.job_description)
        return result
    except Exception as e:
        logger.error(f"Error in job matching: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/get-recommendations")
async def get_recommendations(request: RecommendationsRequest):
    """
    Generate personalized career recommendations

    Args:
        request: Recommendations request

    Returns:
        Personalized recommendations and action plan
    """
    try:
        logger.info(f"Recommendations request received for role: {request.target_role}")
        result = agent.generate_recommendations(request.resume_text, request.target_role, request.industry)
        return result
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/interview-questions")
async def interview_questions(request: InterviewQuestionsRequest):
    """
    Generate tailored interview questions

    Args:
        request: Interview preparation request

    Returns:
        Tailored interview questions
    """
    try:
        logger.info(f"Interview questions request for role: {request.job_title}")
        result = agent.generate_interview_questions(request.job_title, request.skills)
        return result
    except Exception as e:
        logger.error(f"Error generating interview questions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/market-insights")
async def market_insights(request: MarketInsightsRequest):
    """
    Get market insights for skills and industry

    Args:
        request: Market insights request

    Returns:
        Market insights and trends
    """
    try:
        logger.info(f"Market insights request for industry: {request.industry}")
        result = agent.get_market_insights(request.skills, request.industry)
        return result
    except Exception as e:
        logger.error(f"Error getting market insights: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/full-analysis")
async def full_analysis(request: ResumeAnalysisRequest):
    """
    Run complete analysis workflow

    Args:
        request: Full analysis request with resume

    Returns:
        Complete analysis results
    """
    try:
        logger.info("Full analysis request received")

        results = {
            "resume_analysis": agent.analyze_resume(request.resume_text),
            "skills": agent.extract_skills(request.resume_text),
            "recommendations": agent.generate_recommendations(request.resume_text, "Senior Developer"),
        }

        return {"status": "success", "results": results}
    except Exception as e:
        logger.error(f"Error in full analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
