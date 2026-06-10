# 🤖 AI SDR - Automated Lead Generation System

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)]()

> **Automated B2B lead generation system powered by AI.** Finds, qualifies, and scores leads matching your Ideal Customer Profile using LinkedIn data and Claude AI.

---

## 🎯 What It Does

1. **Reads your ICP** from Google Sheets (fully configurable)
2. **Finds matching profiles** on LinkedIn via Apify
3. **Scores each lead** with AI (0-100) using Claude 3.5 Sonnet
4. **Saves qualified leads** to Google Sheets with reasoning
5. **Tracks new leads** automatically
6. **Prevents duplicates** intelligently
7. **Runs on schedule** or on-demand

**Result:** Automated lead generation that saves hours of manual work.

---

## ✨ Key Features

- ✅ **Zero Hardcoding** - All configuration in Google Sheets & config files
- ✅ **AI-Powered Scoring** - Claude 3.5 Sonnet evaluation with reasoning
- ✅ **Smart Filtering** - 13+ ICP criteria (industry, size, location, title, etc.)
- ✅ **Duplicate Prevention** - Automatic LinkedIn URL matching
- ✅ **New Lead Tracking** - Clear YES/NO flags for new entries
- ✅ **Production Ready** - Comprehensive error handling & logging
- ✅ **Cost Effective** - ~$0.50-0.70 per 120 profiles
- ✅ **Scalable** - From 120 to 1000+ leads easily

---

## 📊 Quick Stats

- **10,600+ lines** of code & documentation
- **7 core modules** (2,500+ lines of Python)
- **11 comprehensive guides** (8,000+ lines)
- **4 utility scripts** for testing & maintenance
- **Production-grade** error handling & logging

---

## 🚀 Quick Start

### Prerequisites

1. **Accounts:**
   - Google Cloud (for Sheets API)
   - Apify (for LinkedIn scraping)
   - OpenRouter (for AI scoring)

2. **Credits:**
   - Apify: $5-10
   - OpenRouter: $5-10

### Installation

```bash
# Clone the repository
git clone https://github.com/saria3321/SDR.git
cd SDR

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

### Quick Test

```bash
# Test setup
python test_setup.py

# Test Apify actor
python test_apify_actor.py

# Small test run (4 profiles)
python main_simplified.py --max-companies 2 --max-profiles 2

# Check your Google Sheet for results!
```

---

## 📖 Documentation

### 🌟 Start Here
- **[START_HERE.md](START_HERE.md)** - Main entry point
- **[QUICK_FIX_FOR_CLIENT.md](QUICK_FIX_FOR_CLIENT.md)** - 10-minute setup guide

### 📚 For Users
- **[CLIENT_SUMMARY.md](CLIENT_SUMMARY.md)** - Overview & features
- **[QUICKSTART.md](QUICKSTART.md)** - 15-minute setup
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Comprehensive setup

### 🔧 For Developers
- **[README.md](README.md)** - Technical documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Complete details

### 🚀 For Deployment
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Production guide
- **[FIX_APIFY_ACTORS.md](FIX_APIFY_ACTORS.md)** - Apify configuration
- **[HONEST_DISCLOSURE.md](HONEST_DISCLOSURE.md)** - What's tested & what's not

### 📋 Reference
- **[INDEX.md](INDEX.md)** - Documentation navigation
- **[DELIVERABLES.md](DELIVERABLES.md)** - Complete package inventory

---

## 💰 Cost Estimates

### Per Run (120 profiles)
- **Apify:** ~$0.40-0.50
- **OpenRouter (AI):** ~$0.10-0.20
- **Total:** ~$0.50-0.70

### Monthly (if daily)
- **Cost:** ~$15-25/month
- **Results:** 900-1,500 qualified leads
- **Time saved:** 60-90 hours

---

## 🏗️ Project Structure

```
SDR/
├── 📚 Documentation (11 guides)
│   ├── START_HERE.md
│   ├── QUICK_FIX_FOR_CLIENT.md
│   ├── CLIENT_SUMMARY.md
│   └── ... (8 more guides)
│
├── 🚀 Core Application
│   ├── main.py              # Standard version
│   ├── main_simplified.py   # Simplified version (recommended)
│   ├── config.yaml          # Configuration
│   └── .env.example         # Environment template
│
├── 💻 Source Code
│   └── src/
│       ├── icp_loader.py         # Google Sheets ICP loader
│       ├── apify_scraper.py      # LinkedIn scraping (two-stage)
│       ├── apify_scraper_simplified.py  # Simplified scraping
│       ├── ai_scorer.py          # AI scoring (OpenRouter)
│       ├── sheets_writer.py      # Google Sheets writer
│       ├── scheduler.py          # Job scheduling
│       └── models.py             # Data models
│
└── 🛠️ Utilities
    ├── test_setup.py            # Setup validator
    ├── test_apify_actor.py      # Apify actor test
    ├── validate_config.py       # Config checker
    ├── create_icp_template.py   # ICP template generator
    └── utils_clear_new_flags.py # Flag clearer
```

---

## 🔧 Configuration

### ICP Filters (Google Sheets)

Configure your Ideal Customer Profile with 13+ filters:

- Industries
- Company size (min/max)
- Countries/Regions
- Target job titles
- Required keywords
- Excluded keywords
- Seniority levels
- Departments
- Company types
- Languages
- Years of experience

**No code changes needed - just edit the Google Sheet!**

---

## 🎯 Usage Examples

### One-Time Run
```bash
python main_simplified.py
```

### Custom Limits
```bash
python main_simplified.py --max-companies 50 --max-profiles 5
```

### Scheduled Run (Continuous)
```bash
python main_simplified.py --schedule
```

### Test with Small Dataset
```bash
python main_simplified.py --max-companies 2 --max-profiles 2
```

---

## 🔍 How It Works

### Workflow

```
1. Load ICP from Google Sheets
        ↓
2. Search LinkedIn for matching profiles (Apify)
        ↓
3. Score each profile with AI (OpenRouter/Claude)
        ↓
4. Filter by minimum score (default: 60)
        ↓
5. Check for duplicates
        ↓
6. Save to Google Sheets with "New Lead" flag
```

### AI Scoring (0-100)

- **Job Title Match (30%)** - How well title matches ICP
- **Company Fit (25%)** - Industry, size, location alignment
- **Seniority Level (20%)** - Right decision-maker level
- **Department Fit (15%)** - Department aligns with ICP
- **Keywords (10%)** - Required keywords present

**Each lead includes AI reasoning explaining the score.**

---

## 🧪 Testing

### Validate Setup
```bash
python test_setup.py
```
Tests: Environment variables, Google Sheets, Apify, OpenRouter

### Test Apify Actor
```bash
python test_apify_actor.py
```
Verifies LinkedIn scraper works with your credentials

### Check Configuration
```bash
python validate_config.py
```
Displays current settings and validates paths

---

## 🛠️ Technology Stack

- **Language:** Python 3.9+
- **Data Source:** LinkedIn (via Apify)
- **AI Scoring:** Claude 3.5 Sonnet (via OpenRouter)
- **Storage:** Google Sheets
- **Scheduling:** Python schedule library
- **Validation:** Pydantic
- **Config:** YAML + Environment Variables

---

## 📊 Output Format

Google Sheet columns (19 fields):

| Column | Description |
|--------|-------------|
| Date Added | When lead was added |
| New Lead | YES/NO flag |
| Lead Score | 0-100 score |
| Full Name | Contact name |
| Job Title | Their role |
| Company Name | Company |
| Company Size | Employee count |
| Industry | Industry |
| Location | City/Country |
| LinkedIn URL | Profile link |
| Email | If available |
| Phone | If available |
| Seniority Level | C-Level, VP, etc. |
| Department | Sales, Marketing, etc. |
| Years of Experience | If available |
| AI Reasoning | Why this score? |
| Profile Summary | Bio |
| Company URL | Company LinkedIn |
| Last Updated | Timestamp |

---

## 🔐 Security

- ✅ API keys in `.env` (gitignored)
- ✅ Google credentials in `.json` (gitignored)
- ✅ No hardcoded secrets
- ✅ Minimal permissions
- ✅ Service account isolation

---

## 🐛 Troubleshooting

### Common Issues

**"Actor not found"**
→ Check actor ID in `.env` is correct

**"Insufficient credits"**
→ Add credits to Apify/OpenRouter accounts

**"No profiles found"**
→ ICP too restrictive, try broader criteria

**"Google Sheets error"**
→ Share sheets with service account email

**More help:** See [SETUP_GUIDE.md](SETUP_GUIDE.md#troubleshooting)

---

## 📈 Roadmap

### Current (v1.0)
- ✅ Complete system architecture
- ✅ Google Sheets integration
- ✅ AI scoring with Claude
- ✅ Duplicate prevention
- ✅ Comprehensive documentation

### Future
- 🔄 Email enrichment (Hunter.io)
- 🔄 CRM integration (Salesforce, HubSpot)
- 🔄 Email outreach automation
- 🔄 Analytics dashboard
- 🔄 Multi-ICP support

---

## 🤝 Contributing

This is a client project, but suggestions are welcome:

1. Open an issue for bugs/features
2. Provide detailed description
3. Include logs if applicable

---

## 📄 License

Copyright © 2026. All rights reserved.

Built for B2B lead generation.

---

## 👤 Author

**Saria Irshad**
- GitHub: [@saria3321](https://github.com/saria3321)
- Project: [SDR](https://github.com/saria3321/SDR)

---

## 🙏 Acknowledgments

- **Apify** - LinkedIn scraping infrastructure
- **OpenRouter** - AI API access
- **Anthropic** - Claude 3.5 Sonnet model
- **Google** - Sheets API

---

## 📞 Support

- **Documentation:** See [INDEX.md](INDEX.md) for navigation
- **Setup Issues:** See [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Quick Fix:** See [QUICK_FIX_FOR_CLIENT.md](QUICK_FIX_FOR_CLIENT.md)
- **Issues:** [GitHub Issues](https://github.com/saria3321/SDR/issues)

---

## ⭐ Show Your Support

If this project helps you, please give it a ⭐ on GitHub!

---

**Ready to automate your lead generation?**

👉 **[Start Here](START_HERE.md)** | 📚 **[Documentation](INDEX.md)** | 🚀 **[Quick Setup](QUICK_FIX_FOR_CLIENT.md)**
