# AI SDR - Project Overview

## Project Summary

**Name:** AI SDR - Automated Lead Generation & Qualification System  
**Purpose:** Continuously find and qualify B2B leads matching your Ideal Customer Profile (ICP)  
**Client:** B2B startup in France  
**Delivery:** Complete end-to-end system

---

## What It Does

This system automates the entire lead generation process:

1. **Reads your ICP** from a Google Sheet (fully configurable, no code changes needed)
2. **Finds matching companies** on LinkedIn via Apify scraping
3. **Extracts employee profiles** from those companies matching your target roles
4. **Scores each lead** using AI (OpenRouter/Claude) against your ICP criteria
5. **Saves qualified leads** to Google Sheets with scores and reasoning
6. **Marks new leads** so you know exactly what was added since last run
7. **Prevents duplicates** automatically
8. **Can run on schedule** for continuous lead generation

---

## Key Features

### ✅ Fully Configurable
- ICP settings stored in Google Sheets (edit anytime without touching code)
- All limits configurable (companies, profiles per company, min score)
- Scheduling configurable (on/off, interval)

### ✅ No Hardcoding
- All API keys in environment variables
- All settings in config.yaml
- All ICP criteria in Google Sheets
- Easy to update and maintain

### ✅ Smart Filtering
- **Industries:** Target specific industries
- **Company Size:** Min/max employee count
- **Locations:** Countries/regions
- **Job Titles:** Target decision makers
- **Seniority:** C-Level, VP, Director, etc.
- **Departments:** Sales, Marketing, etc.
- **Keywords:** Required and excluded
- **Experience:** Years of experience range
- **Company Type:** Startup, SMB, Enterprise
- **Languages:** Required languages

### ✅ AI-Powered Scoring
- Each lead scored 0-100 against ICP
- Detailed reasoning provided
- Only qualified leads saved
- Uses Claude 3.5 Sonnet via OpenRouter

### ✅ Google Sheets Integration
- ICP settings in one sheet
- Results automatically in another sheet
- New leads clearly marked
- Duplicate prevention
- No dashboard needed - familiar interface

### ✅ Production Ready
- Comprehensive error handling
- Detailed logging
- Rate limiting
- Retry logic
- Test scripts included
- Setup validators

---

## Technology Stack

### Core Technologies
- **Python 3.9+** - Main programming language
- **Google Sheets API** - Configuration and output
- **Apify** - LinkedIn scraping
- **OpenRouter** - AI scoring (Claude API)

### Key Libraries
- `gspread` - Google Sheets integration
- `apify-client` - Apify API wrapper
- `openai` - OpenRouter API client
- `pydantic` - Data validation
- `schedule` - Job scheduling
- `python-dotenv` - Environment management
- `pyyaml` - Configuration management

---

## Project Structure

```
SDR/
├── main.py                    # Main entry point
├── config.yaml                # Main configuration
├── .env                       # Environment variables (sensitive)
├── .env.example               # Example environment file
├── credentials.json           # Google service account (sensitive)
├── requirements.txt           # Python dependencies
│
├── src/                       # Source code
│   ├── __init__.py
│   ├── models.py              # Data models (Pydantic)
│   ├── icp_loader.py          # Load ICP from Google Sheets
│   ├── apify_scraper.py       # Apify scraping logic
│   ├── ai_scorer.py           # AI scoring with OpenRouter
│   ├── sheets_writer.py       # Write results to Google Sheets
│   └── scheduler.py           # Job scheduling
│
├── logs/                      # Log files
│   └── sdr.log
│
├── README.md                  # Technical documentation
├── SETUP_GUIDE.md             # Detailed setup instructions
├── QUICKSTART.md              # Quick start guide
├── PROJECT_OVERVIEW.md        # This file
│
├── test_setup.py              # Verify setup
├── validate_config.py         # Validate configuration
├── create_icp_template.py     # Generate ICP template
└── utils_clear_new_flags.py   # Utility to clear flags
```

---

## Configuration Files

### 1. `.env` (Environment Variables)
Stores sensitive information:
- API keys (Apify, OpenRouter)
- Google Sheets IDs
- Google credentials path
- Actor IDs

### 2. `config.yaml` (Application Settings)
Stores application settings:
- Limits (max companies, profiles)
- Scheduling (enabled, interval)
- API settings (timeout, retries)
- Scoring thresholds
- Logging configuration

### 3. `credentials.json` (Google Service Account)
Google Cloud service account credentials for Sheets API access.

### 4. Google Sheet: "ICP Settings"
Your Ideal Customer Profile criteria (editable by user):
- Industries, company size, locations
- Job titles, seniority, departments
- Keywords, languages, experience
- All filters optional and flexible

### 5. Google Sheet: "Qualified Leads"
Output sheet with qualified leads:
- Auto-populated by the system
- Includes scores, reasoning, contact info
- Marks new leads
- Prevents duplicates

---

## Data Flow

```
1. User edits ICP Settings (Google Sheet)
        ↓
2. System loads ICP configuration
        ↓
3. Apify searches LinkedIn for matching companies
        ↓
4. Apify extracts employee profiles from companies
        ↓
5. AI scores each profile against ICP (0-100)
        ↓
6. Filter profiles above minimum score
        ↓
7. Check for duplicates in output sheet
        ↓
8. Append new qualified leads to Google Sheet
        ↓
9. Mark new leads with "YES" flag
```

---

## Scoring Algorithm

AI evaluates each lead across 5 dimensions:

1. **Job Title Match (30 points)**
   - How well does the title match target roles?

2. **Company Fit (25 points)**
   - Industry, size, type, location alignment

3. **Seniority Level (20 points)**
   - Right decision-maker level?

4. **Department Fit (15 points)**
   - Department aligns with ICP?

5. **Keywords & Signals (10 points)**
   - Required keywords present?
   - Excluded keywords absent?

**Total Score:** 0-100  
**Default Threshold:** 60 (configurable)

AI also provides reasoning explaining the score.

---

## Cost Estimates

### Per Run (30 companies, 4 profiles each = 120 profiles)

**Apify Costs:**
- Company Search Scraper: ~$0.50-1.00
- Employee Scraper: ~$2.00-3.00
- **Subtotal:** ~$2.50-4.00

**OpenRouter Costs (Claude 3.5 Sonnet):**
- 120 profiles × ~$0.001 each
- **Subtotal:** ~$0.10-0.20

**Total per run:** ~$2.60-4.20

### Monthly Estimates

| Frequency | Runs/Month | Cost/Month |
|-----------|------------|------------|
| Daily | 30 | $78-126 |
| Weekly | 4 | $10-17 |
| Bi-weekly | 2 | $5-8 |

*Costs scale linearly with number of profiles processed.*

---

## Usage Modes

### 1. One-Time Run
```bash
python main.py
```
Run once with config.yaml limits.

### 2. Test Run
```bash
python main.py --max-companies 2 --max-profiles 2
```
Small test with override limits.

### 3. Custom Run
```bash
python main.py --max-companies 50 --max-profiles 5
```
Custom limits from command line.

### 4. Scheduled Run
```bash
python main.py --schedule
```
Runs continuously on schedule (default: every 24 hours).

---

## Output Format

Google Sheet columns:
1. **Date Added** - When lead was added
2. **New Lead** - YES/NO flag
3. **Lead Score** - 0-100
4. **Full Name**
5. **Job Title**
6. **Company Name**
7. **Company Size**
8. **Industry**
9. **Location**
10. **LinkedIn URL** - For outreach
11. **Email** - If available
12. **Phone** - If available
13. **Seniority Level**
14. **Department**
15. **Years of Experience**
16. **AI Reasoning** - Why this score?
17. **Profile Summary**
18. **Company URL**
19. **Last Updated**

---

## Error Handling

### Automatic Recovery
- Retry failed API calls (3 attempts)
- Skip problematic profiles, continue with others
- Log all errors for debugging
- Graceful degradation

### Logging
All activity logged to `logs/sdr.log`:
- Info: Normal operation
- Warning: Recoverable issues
- Error: Failed operations
- Debug: Detailed troubleshooting info

---

## Security & Privacy

### Sensitive Data Protection
- API keys in `.env` (gitignored)
- Credentials in `.json` (gitignored)
- No hardcoded secrets
- Service account with minimum permissions

### Data Handling
- No data stored locally (except logs)
- All results in Google Sheets (user controlled)
- LinkedIn scraping via Apify (compliant)
- No personally identifiable information stored unnecessarily

---

## Maintenance & Updates

### Update ICP
1. Open "ICP Settings" Google Sheet
2. Edit Row 2 with new criteria
3. Save
4. Next run uses new ICP automatically

### Update Limits
1. Edit `config.yaml`
2. Change `max_companies` or `max_profiles_per_company`
3. Next run uses new limits

### Update Scoring Threshold
1. Edit `config.yaml`
2. Change `min_qualified_score`
3. Next run uses new threshold

### Update Schedule
1. Edit `config.yaml`
2. Change `interval_hours`
3. Restart scheduled job

**No code changes needed for any configuration updates!**

---

## Testing & Validation

### Included Test Scripts

1. **test_setup.py**
   - Validates all connections
   - Tests API keys
   - Checks credentials
   - Verifies dependencies

2. **validate_config.py**
   - Shows current configuration
   - Identifies missing values
   - Validates file paths

3. **create_icp_template.py**
   - Creates ICP sheet structure
   - Adds example data
   - Formats headers

4. **utils_clear_new_flags.py**
   - Clears "New Lead" flags
   - Useful after reviewing leads

---

## Scalability

### Current Configuration
- 30 companies × 4 profiles = 120 leads per run
- ~15 minutes execution time
- ~$2.60-4.20 per run

### Can Scale To
- 100+ companies per run
- 10+ profiles per company
- 1000+ leads per run
- Just update `config.yaml`

### Limitations
- Apify rate limits (usually generous)
- OpenRouter rate limits (can upgrade)
- Google Sheets API limits (plenty for this use case)
- LinkedIn may block aggressive scraping (Apify handles this)

---

## Future Enhancements (Optional)

Possible additions (not implemented):

1. **Email Enrichment**
   - Integrate Hunter.io or similar
   - Find email addresses automatically

2. **CRM Integration**
   - Push leads to Salesforce, HubSpot, etc.
   - Sync statuses

3. **Email Outreach**
   - Automated personalized emails
   - Follow-up sequences

4. **Analytics Dashboard**
   - Lead quality metrics
   - Conversion tracking
   - Cost analysis

5. **Multi-ICP Support**
   - Multiple ICP configurations
   - Different target segments

6. **Webhook Notifications**
   - Slack/Discord alerts
   - Email notifications
   - Real-time updates

---

## Support & Documentation

### Documentation Files
- `README.md` - Technical architecture & usage
- `SETUP_GUIDE.md` - Detailed setup instructions (60+ pages)
- `QUICKSTART.md` - Get started in 15 minutes
- `PROJECT_OVERVIEW.md` - This file

### Getting Help
1. Check logs: `logs/sdr.log`
2. Run tests: `python test_setup.py`
3. Validate config: `python validate_config.py`
4. Review setup guide
5. Check error messages

---

## Deliverables Checklist

### ✅ Core System
- [x] ICP loader from Google Sheets
- [x] Apify LinkedIn scraper integration
- [x] AI scoring with OpenRouter
- [x] Google Sheets writer
- [x] Duplicate detection
- [x] New lead marking
- [x] Scheduling system

### ✅ Configuration
- [x] Environment variables (.env)
- [x] YAML configuration (config.yaml)
- [x] No hardcoded values
- [x] Fully configurable limits
- [x] Flexible ICP filters

### ✅ Documentation
- [x] Technical README
- [x] Setup guide
- [x] Quick start guide
- [x] Project overview
- [x] Code comments

### ✅ Testing & Utilities
- [x] Setup validator
- [x] Configuration validator
- [x] ICP template creator
- [x] Utility scripts
- [x] Requirements file

### ✅ Production Ready
- [x] Error handling
- [x] Logging system
- [x] Rate limiting
- [x] Retry logic
- [x] .gitignore file

---

## Success Metrics

### What Success Looks Like
1. System runs without errors
2. Qualified leads appear in Google Sheet
3. Lead scores are relevant (≥60)
4. No duplicates added
5. New leads clearly marked
6. Can modify ICP without code changes
7. Scheduled runs work automatically

### Quality Indicators
- Lead scores above threshold
- AI reasoning makes sense
- Profiles match ICP criteria
- Contact information available
- Company details accurate

---

## Conclusion

This is a complete, production-ready AI SDR system that:

✅ Fully automates lead generation  
✅ Requires no coding to configure  
✅ Scales easily  
✅ Costs ~$3-4 per run  
✅ Integrates with familiar tools (Google Sheets)  
✅ Runs continuously or on-demand  
✅ Prevents duplicates  
✅ Tracks new leads  
✅ Provides AI-powered qualification  

The system replaces manual searching and evaluation, saving hours of work while maintaining high lead quality through AI scoring.

---

**Ready to use. Just follow the QUICKSTART.md guide!**
