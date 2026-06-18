# AI Job Search & Resume Improvement Agent

A multi-agent system that analyzes resumes, extracts skills, searches for relevant jobs, matches job requirements with resume content, and suggests improvements with interview questions.

## Features

- **Resume Analyzer**: Analyzes user resumes for structure and content
- **Skill Extractor**: Automatically extracts skills from resumes
- **Job Finder**: Searches for relevant job opportunities
- **Job-Resume Matcher**: Matches job requirements with resume qualifications
- **Recommendation Agent**: Suggests resume improvements and generates interview questions

## Architecture

This project implements a multi-agent system in three ways:

1. **Langchain Crew AI** - Python-based multi-agent orchestration
2. **Standalone Agent** - Direct implementation with Ollama
3. **N8N Workflow** - Low-code automation workflow

## Tech Stack

- **Ollama** - Local LLM inference
- **Langchain** - LLM framework
- **Crew AI** - Multi-agent orchestration
- **N8N** - Workflow automation
- **Python 3.9+**

## Project Structure

```
.
├── README.md
├── requirements.txt
├── .env.example
├── crew_ai/
│   ├── crew_config.py
│   ├── agents.py
│   ├── tasks.py
│   └── main.py
├── standalone_agent/
│   ├── agent.py
│   ├── utils.py
│   └── main.py
├── n8n/
│   ├── workflow.json
│   ├── setup.md
│   └── docker-compose.yml
├── data/
│   ├── sample_resume.txt
│   └── job_listings.json
└── tests/
    ├── test_crew_agent.py
    └── test_standalone_agent.py
```

## Quick Start

### Prerequisites

1. **Ollama Installation**
   ```bash
   # Download from https://ollama.ai
   # Install and start Ollama service
   ```

2. **Pull Models**
   ```bash
   ollama pull mistral
   ollama pull neural-chat
   ```

3. **Python Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

### Run Crew AI Agent

```bash
cd crew_ai
python main.py
```

### Run Standalone Agent

```bash
cd standalone_agent
python main.py
```

### Run N8N Workflow

```bash
cd n8n
docker-compose up -d
# Visit http://localhost:5678
```

## Environment Variables

Create `.env` file from `.env.example`:

```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
OLLAMA_EMBEDDING_MODEL=neural-chat
JOB_API_KEY=your_job_api_key
JOB_SEARCH_API=https://api.example.com
```

## Agent Roles

### 1. Resume Analyzer
- Analyzes resume structure and content
- Identifies strengths and weaknesses
- Checks formatting and clarity

### 2. Skill Extractor
- Identifies technical and soft skills
- Categorizes skills by level
- Maps skills to industry standards

### 3. Job Finder
- Searches job boards and APIs
- Filters by location, experience, and keywords
- Returns relevant job listings

### 4. Job-Resume Matcher
- Compares resume with job requirements
- Identifies skill gaps
- Calculates match percentage

### 5. Recommendation Agent
- Suggests resume improvements
- Highlights missing skills
- Generates tailored interview questions

## Configuration

### Ollama Configuration

Ollama runs on `http://localhost:11434` by default.

Models used:
- **mistral** - Fast, efficient model for analysis
- **neural-chat** - Optimized for conversational tasks

### Crew AI Configuration

See `crew_ai/crew_config.py` for agent and task configuration.

## Usage Examples

### Python (Crew AI)

```python
from crew_ai.main import run_job_search_agent

result = run_job_search_agent(
    resume_path="path/to/resume.pdf",
    job_preferences={
        "location": "Remote",
        "experience_level": "Mid-Senior",
        "industry": "Tech"
    }
)

print(result)
```

## Testing

```bash
pytest tests/
```

## Troubleshooting

### Ollama Connection Issues
- Ensure Ollama is running: `ollama serve`
- Check connection: `curl http://localhost:11434/api/tags`
- Verify firewall settings

### Model Loading Errors
- Pull required models: `ollama pull mistral`
- Check disk space for model storage
- Review Ollama logs

## Contributing

Contributions welcome! Please:
1. Create a feature branch
2. Make your changes
3. Add tests
4. Submit a pull request

## License

MIT License - See LICENSE file
