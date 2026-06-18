"""
Standalone Job Search Agent
Direct implementation with Ollama without Crew AI
"""

import os
import json
from typing import List, Dict, Any
import requests
from langchain_community.llms import Ollama
from loguru import logger

logger.add("logs/standalone_agent.log")


class JobSearchAgent:
    """Standalone agent for job search and resume analysis"""

    def __init__(self):
        """Initialize the standalone agent with Ollama"""
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "mistral")
        self.temperature = float(os.getenv("OLLAMA_TEMPERATURE", 0.7))

        # Initialize Ollama LLM
        self.llm = Ollama(model=self.model, base_url=self.ollama_base_url, temperature=self.temperature)

        logger.info(f"Agent initialized with model: {self.model}")

    def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """
        Analyze a resume for quality, structure, and effectiveness

        Args:
            resume_text: The resume content to analyze

        Returns:
            Dictionary with analysis results
        """
        logger.info("Starting resume analysis")

        prompt = f"""Analyze the following resume comprehensively and provide:
1. Overall structure and organization (score 0-10)
2. Content quality and effectiveness (score 0-10)
3. ATS compatibility (score 0-10)
4. Key strengths (list top 3)
5. Areas for improvement (list top 3)
6. Overall resume score (0-100)
7. Top 3 actionable recommendations

Resume:
{resume_text}

Provide your analysis in JSON format."""

        try:
            response = self.llm.invoke(prompt)
            logger.info("Resume analysis completed")

            # Parse response
            analysis = {
                "status": "success",
                "analysis": response,
                "model_used": self.model,
            }
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing resume: {str(e)}")
            return {"status": "error", "message": str(e)}

    def extract_skills(self, resume_text: str) -> Dict[str, Any]:
        """
        Extract technical and soft skills from resume

        Args:
            resume_text: The resume content

        Returns:
            Dictionary with extracted skills
        """
        logger.info("Starting skill extraction")

        prompt = f"""Extract all skills from the following resume and categorize them:

1. Technical Skills (with proficiency: Beginner/Intermediate/Advanced/Expert)
2. Soft Skills
3. Tools and Technologies
4. Languages
5. Certifications

Resume:
{resume_text}

Provide output in JSON format with the following structure:
{{
    "technical_skills": [{{"name": "skill", "proficiency": "level"}}],
    "soft_skills": [...],
    "tools_technologies": [...],
    "languages": [...],
    "certifications": [...]
}}"""

        try:
            response = self.llm.invoke(prompt)
            logger.info("Skill extraction completed")

            skills = {
                "status": "success",
                "skills": response,
                "model_used": self.model,
            }
            return skills
        except Exception as e:
            logger.error(f"Error extracting skills: {str(e)}")
            return {"status": "error", "message": str(e)}

    def search_jobs(
        self, skills: List[str], location: str = "Remote", experience_level: str = "Mid"
    ) -> Dict[str, Any]:
        """
        Search for relevant job opportunities

        Args:
            skills: List of skills to search for
            location: Job location preference
            experience_level: Experience level (Junior/Mid/Senior)

        Returns:
            Dictionary with job opportunities
        """
        logger.info(f"Searching for jobs with skills: {skills}")

        prompt = f"""Based on the following skills and preferences, suggest 10 relevant job opportunities:

Skills: {', '.join(skills)}
Location: {location}
Experience Level: {experience_level}

For each job opportunity, provide:
1. Job Title
2. Company (fictional but realistic)
3. Key Requirements
4. Estimated Salary Range
5. Match Score (0-100%)

Format as JSON."""

        try:
            response = self.llm.invoke(prompt)
            logger.info("Job search completed")

            jobs = {
                "status": "success",
                "opportunities": response,
                "model_used": self.model,
            }
            return jobs
        except Exception as e:
            logger.error(f"Error searching jobs: {str(e)}")
            return {"status": "error", "message": str(e)}

    def match_resume_to_job(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """
        Match resume against a job description

        Args:
            resume_text: The resume content
            job_description: The job description

        Returns:
            Dictionary with match analysis
        """
        logger.info("Starting resume-job matching")

        prompt = f"""Compare the following resume with the job description and provide:

1. Overall Match Score (0-100%)
2. Matching Skills (list matching items)
3. Skill Gaps (list missing skills)
4. Experience Alignment (0-100%)
5. Recommendation (Strong/Good/Possible/Poor Match)
6. Priority Improvements for this role (top 3)

Resume:
{resume_text}

Job Description:
{job_description}

Format as JSON."""

        try:
            response = self.llm.invoke(prompt)
            logger.info("Resume-job matching completed")

            match = {
                "status": "success",
                "match_analysis": response,
                "model_used": self.model,
            }
            return match
        except Exception as e:
            logger.error(f"Error matching resume to job: {str(e)}")
            return {"status": "error", "message": str(e)}

    def generate_recommendations(
        self, resume_text: str, target_role: str, industry: str = "Technology"
    ) -> Dict[str, Any]:
        """
        Generate personalized career recommendations

        Args:
            resume_text: The resume content
            target_role: Target job role
            industry: Industry/sector

        Returns:
            Dictionary with recommendations
        """
        logger.info(f"Generating recommendations for role: {target_role}")

        prompt = f"""Based on the following resume, provide comprehensive career recommendations:

Resume:
{resume_text}

Target Role: {target_role}
Industry: {industry}

Provide:
1. Top 5 Resume Improvements (prioritized by impact)
2. Skills to Develop (top 5)
3. Interview Preparation Tips (top 5)
4. Generated Interview Questions (5 questions)
5. Career Development Action Plan:
   - 3-month goals
   - 6-month goals
   - 1-year goals
6. Networking Recommendations
7. Online Presence Tips

Format as JSON."""

        try:
            response = self.llm.invoke(prompt)
            logger.info("Recommendations generated")

            recommendations = {
                "status": "success",
                "recommendations": response,
                "model_used": self.model,
            }
            return recommendations
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return {"status": "error", "message": str(e)}

    def generate_interview_questions(self, job_title: str, skills: List[str]) -> Dict[str, Any]:
        """
        Generate tailored interview questions

        Args:
            job_title: Target job title
            skills: List of relevant skills

        Returns:
            Dictionary with interview questions
        """
        logger.info(f"Generating interview questions for: {job_title}")

        prompt = f"""Generate 15 comprehensive interview questions for a {job_title} position.

Key Skills for this role: {', '.join(skills)}

Include:
1. Technical Questions (5)
2. Behavioral Questions (5)
3. Scenario-Based Questions (5)

For each question provide:
- Question
- Why it's asked
- Good answer points

Format as JSON."""

        try:
            response = self.llm.invoke(prompt)
            logger.info("Interview questions generated")

            questions = {
                "status": "success",
                "interview_questions": response,
                "model_used": self.model,
            }
            return questions
        except Exception as e:
            logger.error(f"Error generating interview questions: {str(e)}")
            return {"status": "error", "message": str(e)}

    def get_market_insights(self, skills: List[str], industry: str = "Technology") -> Dict[str, Any]:
        """
        Get market insights for skills and industry

        Args:
            skills: List of skills
            industry: Industry/sector

        Returns:
            Dictionary with market insights
        """
        logger.info(f"Fetching market insights for industry: {industry}")

        prompt = f"""Provide market insights for the following:

Skills: {', '.join(skills)}
Industry: {industry}

Provide:
1. Skill Demand (which skills are hot)
2. Average Salaries
3. Job Market Outlook
4. Trending Technologies
5. Future-Ready Skills to Learn
6. Geographic Hotspots for these skills
7. Industries hiring for these skills

Format as JSON."""

        try:
            response = self.llm.invoke(prompt)
            logger.info("Market insights retrieved")

            insights = {
                "status": "success",
                "market_insights": response,
                "model_used": self.model,
            }
            return insights
        except Exception as e:
            logger.error(f"Error getting market insights: {str(e)}")
            return {"status": "error", "message": str(e)}
