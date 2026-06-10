# AI SDR - Automated Lead Generation & Qualification System

## Overview
Automated pipeline that finds, qualifies, and scores B2B leads based on your Ideal Customer Profile (ICP). Results are saved to Google Sheets with automatic detection of new leads.

## Features
- ✅ Configurable ICP via Google Sheets (no hardcoding)
- ✅ LinkedIn company discovery using Apify
- ✅ Employee profile extraction per company
- ✅ AI-powered lead scoring using OpenRouter
- ✅ Automatic Google Sheets export with new lead tracking
- ✅ Configurable limits and scheduling
- ✅ Continuous monitoring mode

## Architecture

```
┌─────────────────┐
│  ICP Settings   │  (Google Sheet - editable)
│  - Industries   │
│  - Company Size │
│  - Job Titles   │
│  - Keywords     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Apify LinkedIn Scrapers        │
│  1. Company Search Scraper      │
│     → Find matching companies   │
│  2. Company Employees Scraper   │
│     → Extract target profiles   │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Profile Enrichment             │
│  - Parse profile data           │
│  - Extract key attributes       │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  AI Lead Scoring (OpenRouter)   │
│  - Compare against ICP          │
│  - Generate relevance score     │
│  - Provide reasoning            │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Google Sheets Output           │
│  - Append qualified leads       │
│  - Mark new entries             │
│  - Include score & reasoning    │
└─────────────────────────────────┘
```

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Google Cloud account (for Sheets API)
- Apify account
- OpenRouter API key

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file:
```
APIFY_API_TOKEN=your_apify_token
OPENROUTER_API_KEY=your_openrouter_key
GOOGLE_SHEETS_CREDENTIALS_PATH=credentials.json
ICP_SHEET_ID=your_icp_sheet_id
OUTPUT_SHEET_ID=your_output_sheet_id
```

Create `config.yaml`:
```yaml
limits:
  max_companies: 30
  max_profiles_per_company: 4
  
scheduling:
  enabled: false
  interval_hours: 24
  
apify:
  company_scraper_id: "your_company_scraper_actor_id"
  employee_scraper_id: "your_employee_scraper_actor_id"
  
openrouter:
  model: "anthropic/claude-3.5-sonnet"
  temperature: 0.3
```

### 4. Google Sheets Setup

#### ICP Settings Sheet (Sheet1)
Create a sheet with these columns:
- Industries (e.g., "Software, SaaS, Technology")
- Company Size Min
- Company Size Max
- Countries (e.g., "France, Belgium, Switzerland")
- Target Job Titles (e.g., "CEO, CTO, Founder, VP Sales")
- Required Keywords (e.g., "B2B, Enterprise, SaaS")
- Seniority Levels (e.g., "C-Level, VP, Director")
- Departments (e.g., "Sales, Marketing, Operations")
- Company Types (e.g., "Startup, SMB")
- Languages (e.g., "French, English")
- Excluded Keywords (e.g., "Agency, Freelance")
- Years Experience Min
- Years Experience Max

#### Output Sheet (Sheet2)
Will be automatically populated with:
- Date Added
- New Lead (YES/NO flag)
- Lead Score (0-100)
- Full Name
- Job Title
- Company Name
- Company Size
- Industry
- Location
- LinkedIn URL
- Email (if available)
- Phone (if available)
- Seniority Level
- Department
- Years of Experience
- AI Reasoning
- Profile Summary
- Company URL
- Last Updated

## Usage

### Run Once
```bash
python main.py
```

### Run with Scheduling
```bash
python main.py --schedule
```

### Run with Custom Limits
```bash
python main.py --max-companies 50 --max-profiles 5
```

## Project Structure
```
SDR/
├── main.py                 # Entry point
├── config.yaml            # Configuration
├── .env                   # Environment variables
├── requirements.txt       # Dependencies
├── credentials.json       # Google Service Account
├── src/
│   ├── __init__.py
│   ├── icp_loader.py      # Load ICP from Google Sheets
│   ├── apify_scraper.py   # Apify integration
│   ├── ai_scorer.py       # OpenRouter AI scoring
│   ├── sheets_writer.py   # Google Sheets writer
│   ├── enrichment.py      # Profile enrichment
│   └── scheduler.py       # Job scheduling
├── logs/
│   └── sdr.log
└── README.md
```

## Cost Estimation

### Apify (for 30 companies, 4 profiles each = 120 profiles)
- Company Search: ~$0.50-1.00 per run
- Employee Scraper: ~$2.00-3.00 per run
- **Total per run**: ~$2.50-4.00

### OpenRouter (120 profiles scored)
- Using Claude 3.5 Sonnet: ~$0.10-0.20 per run
- **Total per run**: ~$0.10-0.20

**Total estimated cost per run**: $2.60-4.20

## Monitoring & Logs
Logs are saved to `logs/sdr.log` with detailed execution information.

## License
Proprietary - Built for B2B Lead Generation
