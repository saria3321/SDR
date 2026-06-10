# AI SDR - Quick Start Guide

Get up and running in 15 minutes!

## Prerequisites Checklist
- [ ] Python 3.9+ installed
- [ ] Google account
- [ ] Apify account
- [ ] OpenRouter account

---

## Step-by-Step Setup

### 1. Install Dependencies (2 minutes)
```bash
cd SDR
pip install -r requirements.txt
```

### 2. Setup Google Sheets (5 minutes)

#### Create Sheets
1. Create sheet: "AI SDR - ICP Settings" → Copy Sheet ID from URL
2. Create sheet: "AI SDR - Qualified Leads" → Copy Sheet ID from URL

#### Setup Service Account
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project
3. Enable "Google Sheets API" and "Google Drive API"
4. Create Service Account → Download JSON as `credentials.json`
5. Move `credentials.json` to project folder
6. Share both sheets with service account email (from JSON file)

### 3. Get API Keys (3 minutes)

#### Apify
1. Go to [Apify](https://apify.com/) → Sign up
2. Settings → Integrations → Copy API token

#### OpenRouter
1. Go to [OpenRouter](https://openrouter.ai/) → Sign up
2. Keys → Create Key → Copy API key
3. Credits → Add $5-10

### 4. Configure Environment (2 minutes)

Copy `.env.example` to `.env` and fill in:

```env
APIFY_API_TOKEN=your_apify_token
OPENROUTER_API_KEY=sk-or-v1-your_key
GOOGLE_SHEETS_CREDENTIALS_PATH=credentials.json
ICP_SHEET_ID=your_icp_sheet_id
OUTPUT_SHEET_ID=your_output_sheet_id
ICP_SHEET_TAB_NAME=ICP Settings
OUTPUT_SHEET_TAB_NAME=Qualified Leads
APIFY_COMPANY_SCRAPER_ACTOR=apify/linkedin-company-search-scraper
APIFY_EMPLOYEE_SCRAPER_ACTOR=apify/linkedin-company-employees-scraper
```

### 5. Create ICP Template (1 minute)

```bash
python create_icp_template.py
```

This creates the ICP settings sheet with example data.

### 6. Edit Your ICP (2 minutes)

Open your "AI SDR - ICP Settings" sheet and edit Row 2:

**Example for French B2B SaaS:**
- Industries: `Software, SaaS, Technology`
- Company Size Min: `10`
- Company Size Max: `500`
- Countries: `France, Belgium, Switzerland`
- Target Job Titles: `CEO, CTO, Founder, VP Sales`
- Required Keywords: `B2B, Enterprise, SaaS`
- Seniority Levels: `C-Level, VP, Director, Founder`
- Departments: `Sales, Marketing`
- Company Types: `Startup, SMB`
- Languages: `French, English`
- Excluded Keywords: `Agency, Freelance`
- Years Experience Min: `3`
- Years Experience Max: `20`

### 7. Test Setup (1 minute)

```bash
python test_setup.py
```

Should show all ✓ PASS.

### 8. Run Test (2 minutes)

Small test run:
```bash
python main.py --max-companies 2 --max-profiles 2
```

This will:
- Scrape 2 companies
- Get 2 profiles per company (4 total)
- Score with AI
- Write to Google Sheets

Check your "AI SDR - Qualified Leads" sheet!

---

## First Full Run

Once testing works:

```bash
python main.py
```

This runs with default limits (30 companies, 4 profiles each = 120 profiles).

**Estimated time:** 10-15 minutes  
**Estimated cost:** $2.50-4.20

---

## Results

Open your "AI SDR - Qualified Leads" sheet to see:
- New qualified leads with "New Lead" = YES
- Lead scores (0-100)
- AI reasoning for each score
- Full profile details
- LinkedIn URLs for outreach

---

## Common Issues

### "Permission Denied" on Google Sheets
→ Share both sheets with service account email (Editor access)

### "Apify credits exhausted"
→ Add credits in Apify dashboard

### "OpenRouter authentication failed"
→ Check API key in .env starts with `sk-or-v1-`

### "No companies found"
→ ICP too restrictive, try broader criteria

---

## Next Steps

### Optimize ICP
Refine your ICP settings based on results quality.

### Adjust Scoring
Edit `config.yaml` to change `min_qualified_score` (default: 60).

### Scale Up
Increase limits in `config.yaml`:
```yaml
limits:
  max_companies: 50
  max_profiles_per_company: 5
```

### Automate
Run on schedule:
```bash
python main.py --schedule
```

Runs every 24 hours (configurable in `config.yaml`).

---

## Support

- Check logs: `logs/sdr.log`
- Full guide: `SETUP_GUIDE.md`
- Architecture: `README.md`

Happy lead hunting! 🎯
