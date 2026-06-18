"""
Standalone Agent Main Entry Point
CLI interface for job search and resume analysis
"""

import sys
import json
import click
from pathlib import Path
from standalone_agent.agent import JobSearchAgent
from standalone_agent.utils import load_resume_from_file, save_analysis_report
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


@click.group()
def cli():
    """Job Search & Resume Improvement Agent"""
    pass


@cli.command()
@click.option("--resume", type=click.Path(exists=True), help="Path to resume file")
def analyze(resume):
    """Analyze a resume"""
    console.print(Panel.fit("📋 Resume Analysis", style="bold cyan"))

    try:
        if not resume:
            resume_text = click.prompt("Paste your resume content (press Enter twice to finish)")
        else:
            resume_text = load_resume_from_file(resume)

        agent = JobSearchAgent()
        result = agent.analyze_resume(resume_text)

        if result["status"] == "success":
            console.print(Panel(result["analysis"], title="Analysis Results", style="green"))
            save_analysis_report(result)
        else:
            console.print(f"[red]Error: {result['message']}[/red]")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


@cli.command()
@click.option("--resume", type=click.Path(exists=True), required=True, help="Path to resume file")
def extract_skills(resume):
    """Extract skills from resume"""
    console.print(Panel.fit("🎯 Skill Extraction", style="bold cyan"))

    try:
        resume_text = load_resume_from_file(resume)
        agent = JobSearchAgent()
        result = agent.extract_skills(resume_text)

        if result["status"] == "success":
            console.print(Panel(result["skills"], title="Extracted Skills", style="green"))
            save_analysis_report(result, "skills_report.json")
        else:
            console.print(f"[red]Error: {result['message']}[/red]")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


@cli.command()
@click.option("--skills", multiple=True, required=True, help="Skills to search for")
@click.option("--location", default="Remote", help="Job location")
@click.option("--experience", default="Mid", help="Experience level")
def search_jobs(skills, location, experience):
    """Search for jobs"""
    console.print(Panel.fit("🔍 Job Search", style="bold cyan"))

    try:
        agent = JobSearchAgent()
        result = agent.search_jobs(list(skills), location, experience)

        if result["status"] == "success":
            console.print(
                Panel(result["opportunities"], title="Job Opportunities", style="green")
            )
            save_analysis_report(result, "jobs_report.json")
        else:
            console.print(f"[red]Error: {result['message']}[/red]")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


@cli.command()
@click.option("--resume", type=click.Path(exists=True), required=True, help="Path to resume file")
@click.option("--job", type=click.Path(exists=True), required=True, help="Path to job description file")
def match(resume, job):
    """Match resume to job"""
    console.print(Panel.fit("🔗 Resume-Job Matching", style="bold cyan"))

    try:
        resume_text = load_resume_from_file(resume)
        job_text = load_resume_from_file(job)

        agent = JobSearchAgent()
        result = agent.match_resume_to_job(resume_text, job_text)

        if result["status"] == "success":
            console.print(Panel(result["match_analysis"], title="Match Analysis", style="green"))
            save_analysis_report(result, "match_report.json")
        else:
            console.print(f"[red]Error: {result['message']}[/red]")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


@cli.command()
@click.option("--resume", type=click.Path(exists=True), required=True, help="Path to resume file")
@click.option("--role", required=True, help="Target job role")
@click.option("--industry", default="Technology", help="Industry")
def recommend(resume, role, industry):
    """Get career recommendations"""
    console.print(Panel.fit("💡 Career Recommendations", style="bold cyan"))

    try:
        resume_text = load_resume_from_file(resume)
        agent = JobSearchAgent()
        result = agent.generate_recommendations(resume_text, role, industry)

        if result["status"] == "success":
            console.print(
                Panel(result["recommendations"], title="Recommendations", style="green")
            )
            save_analysis_report(result, "recommendations_report.json")
        else:
            console.print(f"[red]Error: {result['message']}[/red]")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


@cli.command()
@click.option("--role", required=True, help="Job role")
@click.option("--skills", multiple=True, required=True, help="Required skills")
def interview_prep(role, skills):
    """Generate interview questions"""
    console.print(Panel.fit("🎤 Interview Preparation", style="bold cyan"))

    try:
        agent = JobSearchAgent()
        result = agent.generate_interview_questions(role, list(skills))

        if result["status"] == "success":
            console.print(
                Panel(result["interview_questions"], title="Interview Questions", style="green")
            )
            save_analysis_report(result, "interview_questions.json")
        else:
            console.print(f"[red]Error: {result['message']}[/red]")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


@cli.command()
@click.option("--skills", multiple=True, required=True, help="Skills to analyze")
@click.option("--industry", default="Technology", help="Industry")
def market_insights(skills, industry):
    """Get market insights"""
    console.print(Panel.fit("📊 Market Insights", style="bold cyan"))

    try:
        agent = JobSearchAgent()
        result = agent.get_market_insights(list(skills), industry)

        if result["status"] == "success":
            console.print(Panel(result["market_insights"], title="Market Insights", style="green"))
            save_analysis_report(result, "market_insights.json")
        else:
            console.print(f"[red]Error: {result['message']}[/red]")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


@cli.command()
@click.option("--resume", type=click.Path(exists=True), required=True, help="Path to resume file")
@click.option("--role", required=True, help="Target job role")
@click.option("--location", default="Remote", help="Job location")
@click.option("--experience", default="Mid", help="Experience level")
def full_analysis(resume, role, location, experience):
    """Run complete analysis workflow"""
    console.print(Panel.fit("🚀 Full Job Search Analysis", style="bold blue"))

    try:
        resume_text = load_resume_from_file(resume)
        agent = JobSearchAgent()

        console.print("\n[cyan]Step 1: Analyzing Resume...[/cyan]")
        analysis = agent.analyze_resume(resume_text)
        console.print("✅ Resume analysis complete\n")

        console.print("[cyan]Step 2: Extracting Skills...[/cyan]")
        skills = agent.extract_skills(resume_text)
        console.print("✅ Skills extraction complete\n")

        console.print("[cyan]Step 3: Generating Recommendations...[/cyan]")
        recommendations = agent.generate_recommendations(resume_text, role)
        console.print("✅ Recommendations generated\n")

        console.print("[cyan]Step 4: Preparing Interview Questions...[/cyan]")
        interview_questions = agent.generate_interview_questions(role, ["Python", "Leadership"])
        console.print("✅ Interview questions generated\n")

        # Compile results
        full_report = {
            "resume_analysis": analysis,
            "skills": skills,
            "recommendations": recommendations,
            "interview_questions": interview_questions,
        }

        save_analysis_report(full_report, "full_analysis_report.json")
        console.print("[green]✨ Full analysis complete! Check full_analysis_report.json[/green]")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


if __name__ == "__main__":
    cli()
