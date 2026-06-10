# 🎯 AI SDR System - Ready for Testing

## ✅ System Status: Configured & Ready

Your AI SDR system is configured with your credentials and ready to test!

---

## 📦 What You Have

### Complete System
- ✅ All source code (18 files)
- ✅ Your credentials configured
- ✅ Professional README
- ✅ Test scripts included
- ✅ GitHub repository: https://github.com/saria3321/SDR

### Your Credentials (Configured)
- ✅ Apify API Token
- ✅ OpenRouter API Key  
- ✅ Google Service Account
- ✅ Google Sheets IDs

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Share Google Sheets ⚠️ MUST DO

Open both sheets and share with this email:
```
hyvop-ai-automation@hyvop-481511.iam.gserviceaccount.com
```

**Give "Editor" permissions**

**Your Sheets:**
- ICP Sheet: https://docs.google.com/spreadsheets/d/1Z1N2p8t0iUB2FaldGcpDGsu7qbbKTJ-LfB6PQKn7v3Y
- Output Sheet: https://docs.google.com/spreadsheets/d/1wIzjo9vJfAZiutLxeSv_0zqGviGwFFrK7DkP3lSrUxc

### Step 2: Set Up ICP Sheet

In your ICP Sheet:
1. Create a tab called "ICP Settings"
2. **Row 1 (Headers):**
   ```
   Industries | Company Size Min | Company Size Max | Countries | Target Job Titles | Required Keywords | Seniority Levels | Departments | Company Types | Languages | Excluded Keywords | Years Experience Min | Years Experience Max
   ```

3. **Row 2 (Your Data) - Example:**
   ```
   Software, SaaS | 10 | 500 | France, Belgium | CEO, CTO, VP Sales | B2B, Enterprise | C-Level, VP | Sales, Marketing | Startup, SMB | French, English | Agency, Freelance | 3 | 20
   ```

### Step 3: Install Dependencies

```bash
cd SDR
pip install google-auth google-auth-oauthlib google-api-python-client gspread apify-client python-dotenv pyyaml requests schedule pydantic
```

### Step 4: Run Test

```bash
python main_simplified.py --max-companies 2 --max-profiles 2
```

This will:
- Search for 4 profiles (2 companies × 2 profiles)
- Score them with AI
- Save to your Output Sheet
- Cost: ~$0.12

### Step 5: Check Results

Open your Output Sheet - you should see qualified leads with:
- Names, titles, companies
- LinkedIn URLs
- Scores (0-100)
- AI reasoning

---

## 💰 Cost Reference

### Test Run (4 profiles)
- Apify: ~$0.10
- OpenRouter: ~$0.02
- **Total: ~$0.12**

### Full Run (120 profiles)
- Apify: ~$0.40-0.50
- OpenRouter: ~$0.10-0.20
- **Total: ~$0.50-0.70**

---

## 🎯 Usage Commands

```bash
# Test run (4 profiles)
python main_simplified.py --max-companies 2 --max-profiles 2

# Standard run (120 profiles)
python main_simplified.py

# Custom run (200 profiles)
python main_simplified.py --max-companies 50 --max-profiles 4

# Scheduled run (continuous, every 24 hours)
python main_simplified.py --schedule
```

---

## 📊 What You'll Get

### In Your Output Sheet:
- Date Added
- New Lead (YES/NO)
- Lead Score (0-100)
- Full Name
- Job Title
- Company Name
- Company Size
- Industry
- Location
- LinkedIn URL (for outreach)
- Email (if available)
- Phone (if available)
- Seniority Level
- Department
- AI Reasoning
- Profile Summary

**Ready for immediate outreach!**

---

## 🔧 Configuration

### Adjust Limits
Edit `config.yaml`:
```yaml
limits:
  max_companies: 30
  max_profiles_per_company: 4

scoring:
  min_qualified_score: 60  # Adjust threshold
```

### Update ICP
Just edit your Google Sheet - no code changes needed!

---

## 🐛 Troubleshooting

### "Permission Denied" (Google Sheets)
→ Share both sheets with service account email (see Step 1)

### "Insufficient credits"
→ Add credits to Apify ($5-10) and OpenRouter ($5-10)

### "No profiles found"
→ ICP too restrictive, try broader criteria

### "Module not found"
→ Run: `pip install -r requirements.txt`

---

## 📁 Important Files

- **README.md** - Complete documentation
- **SETUP_STATUS.md** - Detailed setup instructions
- **main_simplified.py** - Main application
- **config.yaml** - Configuration settings
- **.env** - Your credentials (already configured)
- **credentials.json** - Google auth (already configured)

---

## 🎓 How It Works

```
1. Loads your ICP from Google Sheet
        ↓
2. Searches LinkedIn for matching profiles
        ↓
3. Scores each profile with AI (0-100)
        ↓
4. Filters by minimum score (60)
        ↓
5. Checks for duplicates
        ↓
6. Saves to Google Sheet with "New Lead" flag
```

---

## ✅ Checklist

Before running:
- [ ] Google Sheets shared with service account
- [ ] ICP data in "ICP Settings" tab
- [ ] Dependencies installed
- [ ] $5-10 credits in Apify account
- [ ] $5-10 credits in OpenRouter account

Ready to run:
- [ ] Run test: `python main_simplified.py --max-companies 2 --max-profiles 2`
- [ ] Check Output Sheet for results
- [ ] Adjust ICP if needed
- [ ] Scale up for full run

---

## 🎉 You're Ready!

Everything is configured. Just:
1. ✅ Share Google Sheets
2. ✅ Set up ICP data
3. ✅ Install dependencies
4. ✅ Run test!

**Your automated lead generation system is ready to go!** 🚀

---

## 📞 Support

- **Documentation:** See README.md
- **Configuration:** See SETUP_STATUS.md
- **Repository:** https://github.com/saria3321/SDR
- **Quick Test:** `python simple_test.py`

---

**Questions? All documentation is in the project folder. Happy lead hunting!** 🎯
