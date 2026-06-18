# N8N Workflow Setup Guide

## Overview

This directory contains the N8N workflow for the Job Search & Resume Improvement Agent. N8N is a low-code workflow automation platform that allows you to create complex automation workflows without writing code.

## Prerequisites

1. **Docker & Docker Compose** - For running N8N
2. **Ollama Service** - Running on localhost:11434
3. **Python FastAPI Server** - Running on localhost:8000 (optional, for API integration)

## Quick Start

### 1. Start N8N with Docker Compose

```bash
# Navigate to this directory
cd n8n

# Start N8N
docker-compose up -d

# Check if running
docker-compose ps

# View logs
docker-compose logs -f n8n
```

### 2. Access N8N

Open your browser and navigate to:
```
http://localhost:5678
```

### 3. Import Workflow

1. In N8N dashboard, click **"Open"** or **"Import from File"**
2. Select `workflow.json`
3. Review the workflow connections
4. Click **"Save"**

### 4. Configure API Keys

Edit the workflow nodes to add:
- **Ollama Base URL**: http://localhost:11434
- **FastAPI Base URL**: http://localhost:8000 (if using API)
- **Job API Keys**: If integrating with external job boards

## Workflow Structure

### Trigger Nodes

1. **Manual Trigger** - For manual workflow execution
2. **Webhook** - For external triggers
3. **Schedule** - For automated scheduling

### Processing Nodes

#### Stage 1: Resume Input
- File upload node or text input
- Resume parsing

#### Stage 2: Analysis (Parallel Processing)
- **Resume Analyzer Node** - Analyzes resume structure
- **Skill Extractor Node** - Extracts skills in parallel
- **Market Insights Node** - Gets current market data

#### Stage 3: Job Search & Matching
- **Job Search Node** - Searches for relevant opportunities
- **Job Matcher Node** - Matches resume with jobs
- **Score Calculator** - Calculates match percentages

#### Stage 4: Recommendations
- **Recommendation Generator** - Creates personalized advice
- **Interview Question Generator** - Generates practice questions

#### Stage 5: Output
- **Email Notification** - Sends results via email
- **Slack Integration** - Posts to Slack channel
- **Database Save** - Stores results in database
- **JSON Output** - Returns structured results

## Node Configuration Examples

### HTTP Request Node (for Ollama)

```
Method: POST
URL: http://localhost:11434/api/generate
Headers:
  Content-Type: application/json
Body:
{
  "model": "mistral",
  "prompt": "Analyze this resume: {{$node.resumeInput.json.text}}",
  "stream": false
}
```

### HTTP Request Node (for FastAPI)

```
Method: POST
URL: http://localhost:8000/api/analyze-resume
Headers:
  Content-Type: application/json
Body:
{
  "resume_text": "{{$node.resumeInput.json.text}}"
}
```

### Function Node (for Data Transformation)

```javascript
return {
  resume_text: $node.resumeUpload.json.body,
  analysis_timestamp: new Date().toISOString(),
  processing_status: "started"
};
```

## Environment Variables

Create `.env` file for N8N container:

```env
OLLAMA_BASE_URL=http://host.docker.internal:11434
FASTAPI_BASE_URL=http://host.docker.internal:8000
JOB_API_KEY=your_api_key
SLACK_WEBHOOK=your_webhook_url
EMAIL_FROM=your_email@example.com
EMAIL_PASSWORD=your_password
```

## Workflow Execution

### Manual Execution

1. Open workflow in N8N
2. Click **"Execute Workflow"** button
3. Provide input data
4. View execution log in real-time

### Scheduled Execution

1. Open workflow
2. Click **"Schedule"** tab
3. Set trigger frequency (hourly, daily, weekly)
4. Click **"Activate Workflow"**

### Webhook Trigger

1. Get webhook URL from N8N workflow
2. Configure external system to POST to webhook
3. Workflow executes automatically on trigger

## Integration Examples

### Slack Integration

Send results to Slack channel:

```javascript
{
  "channel": "#job-search",
  "text": "Resume Analysis Complete",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": `*Resume Score:* ${$node.analysis.json.score}\n*Match:* ${$node.matching.json.percentage}%`
      }
    }
  ]
}
```

### Email Integration

Send detailed report via email:

```
To: candidate@example.com
Subject: Your Job Search Analysis - {{$now.format('YYYY-MM-DD')}}
Body: 
Dear {{$node.input.json.name}},

Your resume analysis is ready:
- Overall Score: {{$node.analysis.json.score}}/100
- Top Match: {{$node.matching.json.top_job.title}}
- Match Percentage: {{$node.matching.json.percentage}}%

Best regards,
Job Search Agent
```

### Database Integration

Store results in PostgreSQL:

```sql
INSERT INTO analyses (
  user_id, resume_text, analysis_results, 
  skills, job_matches, created_at
) VALUES (
  '{{$node.auth.json.user_id}}',
  '{{$node.resumeInput.json.text}}',
  '{{$node.analysis.json}}',
  '{{$node.skills.json}}',
  '{{$node.matching.json}}',
  NOW()
)
```

## Workflow Templates

### Template 1: Resume Analysis Only

Simple workflow for quick resume analysis:
- Input: Resume text
- Processing: Resume Analyzer
- Output: Analysis results

### Template 2: Full Job Search Workflow

Complete workflow with all features:
- Input: Resume + Preferences
- Processing: All analysis nodes
- Output: Email report + Slack notification

### Template 3: Scheduled Job Monitoring

Continuous job monitoring:
- Trigger: Daily schedule
- Processing: Search + Match
- Output: Database + Email alerts

## Debugging

### View Workflow Logs

```bash
docker-compose logs n8n | grep ERROR
```

### Test Individual Nodes

1. Right-click node
2. Select "Execute Node"
3. View output in panel

### Enable Debug Mode

```bash
docker-compose down
export DEBUG=*
docker-compose up
```

## Performance Optimization

### Parallel Execution

Use parallel nodes for simultaneous processing:
- Analyzer + Skill Extractor
- Multiple job searches
- Batch processing

### Caching

Cache results to avoid redundant API calls:
- Store resume analyses
- Cache skill extractions
- Use conditional logic

### Rate Limiting

Set rate limits for external APIs:
- 60 requests/minute for most APIs
- 10 requests/second for Ollama
- Implement backoff strategies

## Troubleshooting

### Container Won't Start

```bash
docker-compose down
docker-compose up --build
```

### Connection Refused

Check if services are running:
```bash
curl http://localhost:5678  # N8N
curl http://localhost:11434/api/tags  # Ollama
curl http://localhost:8000/health  # FastAPI
```

### Timeout Errors

Increase timeout in HTTP nodes:
- Set timeout to 60000ms (60 seconds)
- Add retry logic with exponential backoff

### Memory Issues

Adjust Docker resources:
```yaml
services:
  n8n:
    mem_limit: 2g
    memswap_limit: 2g
```

## Resources

- [N8N Documentation](https://docs.n8n.io)
- [N8N Community](https://community.n8n.io)
- [N8N Workflows Gallery](https://n8n.io/workflows)
- [Ollama Documentation](https://ollama.ai)

## Support

For issues or questions:
1. Check N8N logs: `docker-compose logs n8n`
2. Review workflow connections
3. Test API endpoints manually
4. Check GitHub issues

## License

Same as main project - MIT License
