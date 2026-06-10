# AI SDR - Complete Setup Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Google Sheets Setup](#google-sheets-setup)
3. [Apify Setup](#apify-setup)
4. [OpenRouter Setup](#openrouter-setup)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [Running the System](#running-the-system)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Accounts
- **Google Cloud Account** (for Sheets API)
- **Apify Account** (for LinkedIn scraping)
- **OpenRouter Account** (for AI scoring)

### Software Requirements
- Python 3.9 or higher
- pip (Python package manager)
- Git (optional, for version control)

---

## Google Sheets Setup

### 1. Create Google Sheets

#### A. ICP Settings Sheet
1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet named "AI SDR - ICP Settings"
3. In the first tab, rename it to "ICP Settings"
4. Add the following headers in Row 1:

| Industries | Company Size Min | Company Size Max | Countries | Target Job Titles | Required Keywords | Seniority Levels | Departments | Company Types | Languages | Excluded Keywords | Years Experience Min | Years Experience Max |
|------------|------------------|------------------|-----------|-------------------|-------------------|------------------|-------------|---------------|-----------|-------------------|---------------------|---------------------|

5. Fill in Row 2 with your ICP criteria. Example:

| Industries | Company Size Min | Company Size Max | Countries | Target Job Titles | Required Keywords | Seniority Levels | Departments | Company Types | Languages | Excluded Keywords | Years Experience Min | Years Experience Max |
|------------|------------------|------------------|-----------|-------------------|-------------------|------------------|-------------|---------------|-----------|-------------------|---------------------|---------------------|
| Software, SaaS, Technology | 10 | 500 | France, Belgium, Switzerland | CEO, CTO, Founder, VP Sales, Head of Sales | B2B, Enterprise, SaaS | C-Level, VP, Director, Founder | Sales, Marketing, Operations | Startup, SMB | French, English | Agency, Freelance | 3 | 20 |

6. Note the **Sheet ID** from the URL (the long string between `/d/` and `/edit`)

#### B. Output Sheet
1. Create another new spreadsheet named "AI SDR - Qualified Leads"
2. Leave it empty (headers will be created automatically)
3. Note the **Sheet ID** from the URL

### 2. Setup Google Cloud Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable APIs:
   - Go to "APIs & Services" > "Library"
   - Search and enable "Google Sheets API"
   - Search and enable "Google Drive API"
4. Create Service Account:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Name: `ai-sdr-service`
   - Click "Create and Continue"
   - Skip roles and permissions
   - Click "Done"
5. Create Key:
   - Click on the service account you just created
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key"
   - Choose "JSON"
   - Save the file as `credentials.json`
6. Share Sheets with Service Account:
   - Open the service account JSON file
   - Copy the `client_email` value (looks like: `ai-sdr-service@project-id.iam.gserviceaccount.com`)
   - Go to both Google Sheets (ICP and Output)
   - Click "Share" button
   - Paste the service account email
   - Give "Editor" permissions
   - Uncheck "Notify people"
   - Click "Share"

---

## Apify Setup

### 1. Create Apify Account
1. Go to [Apify](https://apify.com/)
2. Sign up for a free account
3. Verify your email

### 2. Get API Token
1. Go to Settings > Integrations
2. Copy your "Personal API token"

### 3. Subscribe to LinkedIn Scrapers
The system uses two Apify actors:

#### Option 1: Official Apify Actors (Recommended)
1. **LinkedIn Company Search Scraper**
   - Search for "LinkedIn Company Search" in Apify Store
   - Subscribe to the actor (may require paid plan)
   - Note the actor ID (usually: `apify/linkedin-company-search-scraper`)

2. **LinkedIn Company Employees Scraper**
   - Search for "LinkedIn Company Employees" in Apify Store
   - Subscribe to the actor
   - Note the actor ID (usually: `apify/linkedin-company-employees-scraper`)

#### Option 2: Alternative Scrapers
If the above are unavailable, search for equivalent scrapers in the Apify Store that can:
- Search LinkedIn companies by criteria
- Extract employee profiles from company pages

### 4. Cost Estimation
- Apify operates on a credit system
- Typical cost: $2-4 per run (30 companies, 120 profiles)
- Free tier includes $5 credits/month
- Consider upgrading to paid plan for regular use

---

## OpenRouter Setup

### 1. Create Account
1. Go to [OpenRouter](https://openrouter.ai/)
2. Sign up with email or GitHub

### 2. Get API Key
1. Go to "Keys" section
2. Click "Create Key"
3. Name it "AI SDR"
4. Copy the API key (starts with `sk-or-v1-...`)

### 3. Add Credits
1. Go to "Credits" section
2. Add credits ($5-10 recommended to start)
3. Cost per run: ~$0.10-0.20 for 120 profiles

---

## Installation

### 1. Clone or Download Project
```bash
cd /path/to/your/projects
# If using git:
git clone <repository-url> ai-sdr
cd ai-sdr

# Or download and extract the ZIP file
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add Credentials File
- Move the `credentials.json` file from Google Cloud setup to the project root
- Path should be: `ai-sdr/credentials.json`

---

## Configuration

### 1. Create .env File
Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
# Apify Configuration
APIFY_API_TOKEN=your_actual_apify_token

# OpenRouter Configuration
OPENROUTER_API_KEY=sk-or-v1-your_actual_key

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS_PATH=credentials.json
ICP_SHEET_ID=your_icp_sheet_id_from_url
OUTPUT_SHEET_ID=your_output_sheet_id_from_url

# ICP Sheet Tab Names
ICP_SHEET_TAB_NAME=ICP Settings
OUTPUT_SHEET_TAB_NAME=Qualified Leads

# Apify Actor IDs
APIFY_COMPANY_SCRAPER_ACTOR=apify/linkedin-company-search-scraper
APIFY_EMPLOYEE_SCRAPER_ACTOR=apify/linkedin-company-employees-scraper
```

### 2. Verify config.yaml
The `config.yaml` file contains all non-sensitive settings. Default values should work, but you can adjust:

```yaml
limits:
  max_companies: 30              # Adjust based on needs
  max_profiles_per_company: 4    # Adjust based on needs

scheduling:
  enabled: false
  interval_hours: 24             # How often to run (if scheduled)

scoring:
  min_qualified_score: 60        # Minimum score to qualify (0-100)
```

---

## Running the System

### 1. Test Configuration
First, verify everything is set up correctly:

```bash
python main.py --max-companies 2 --max-profiles 2
```

This will:
- Test Google Sheets connection
- Test ICP loading
- Scrape 2 companies
- Extract 2 profiles per company
- Score with AI
- Write to Google Sheets

### 2. Full Run
Once testing works:

```bash
python main.py
```

This uses the limits from `config.yaml` (default: 30 companies, 4 profiles each)

### 3. Custom Limits
Override limits from command line:

```bash
python main.py --max-companies 50 --max-profiles 5
```

### 4. Scheduled Mode
Run continuously on a schedule:

```bash
python main.py --schedule
```

This will:
- Run immediately
- Then run every 24 hours (configurable in `config.yaml`)
- Continue until stopped with Ctrl+C

### 5. Check Results
1. Open your "AI SDR - Qualified Leads" Google Sheet
2. Look for entries with "New Lead" = YES
3. Leads are sorted with newest at the bottom
4. Check the "Lead Score" and "AI Reasoning" columns

---

## Troubleshooting

### Common Issues

#### 1. Google Sheets Permission Denied
**Error:** `gspread.exceptions.APIError: 403`

**Solution:**
- Make sure you shared both sheets with the service account email
- Check that the service account has "Editor" permissions
- Verify the Sheet IDs in `.env` are correct

#### 2. Apify Credits Exhausted
**Error:** `Insufficient credits`

**Solution:**
- Add more credits to your Apify account
- Reduce `max_companies` and `max_profiles_per_company` in config

#### 3. OpenRouter Rate Limit
**Error:** `Rate limit exceeded`

**Solution:**
- Add delay between requests (automatic in code)
- Upgrade OpenRouter plan
- Use a cheaper model in `config.yaml`

#### 4. No Companies Found
**Problem:** Scraper returns 0 companies

**Solution:**
- Check your ICP settings are not too restrictive
- Verify industries and countries are spelled correctly
- Try broader search criteria

#### 5. LinkedIn Blocking
**Problem:** Apify actors fail or return empty results

**Solution:**
- LinkedIn may be blocking scraping attempts
- Try running at different times
- Use premium Apify actors with better proxies
- Contact Apify support

#### 6. Low Quality Scores
**Problem:** All leads score below 60

**Solution:**
- Review your ICP settings (might be too strict)
- Lower `min_qualified_score` in `config.yaml`
- Adjust target job titles to match common LinkedIn titles

### Check Logs
All activity is logged to `logs/sdr.log`:

```bash
# View recent logs
tail -n 50 logs/sdr.log

# Follow logs in real-time
tail -f logs/sdr.log
```

### Test Individual Components

#### Test ICP Loading
```python
python -c "
from src.icp_loader import ICPLoader
import os
from dotenv import load_dotenv

load_dotenv()
loader = ICPLoader(
    os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH'),
    os.getenv('ICP_SHEET_ID')
)
icp = loader.load_icp()
print(f'Industries: {icp.industries}')
print(f'Job Titles: {icp.target_job_titles}')
"
```

#### Test Google Sheets Connection
```python
python -c "
from src.sheets_writer import SheetsWriter
import os
from dotenv import load_dotenv

load_dotenv()
writer = SheetsWriter(
    os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH'),
    os.getenv('OUTPUT_SHEET_ID')
)
writer.initialize_sheet()
print('Sheet initialized successfully!')
"
```

---

## Support

For issues or questions:
1. Check the logs in `logs/sdr.log`
2. Review this setup guide
3. Check the README.md for architecture details
4. Verify all API keys and credentials are correct

---

## Next Steps

Once everything is working:
1. **Optimize ICP Settings:** Refine your criteria based on results
2. **Adjust Scoring:** Modify `min_qualified_score` based on lead quality
3. **Scale Up:** Increase limits once you're confident
4. **Automate:** Use scheduled mode for continuous lead generation
5. **Monitor Costs:** Track Apify and OpenRouter usage

Happy lead hunting! 🎯
