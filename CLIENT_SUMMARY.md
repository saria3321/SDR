# AI SDR System - Client Summary

## 🎯 What You're Getting

A complete, production-ready AI-powered lead generation system that automatically:

1. ✅ Finds companies matching your Ideal Customer Profile (ICP)
2. ✅ Extracts employee profiles from those companies
3. ✅ Scores each lead with AI (0-100)
4. ✅ Saves qualified leads to Google Sheets
5. ✅ Marks new leads so you know what's fresh
6. ✅ Prevents duplicates automatically
7. ✅ Can run on schedule (daily, weekly, etc.)

**No coding required to configure - everything is in Google Sheets and config files.**

---

## 📊 How It Works

```
Your ICP (Google Sheet)
         ↓
Find Companies (Apify + LinkedIn)
         ↓
Extract Profiles (Apify + LinkedIn)
         ↓
Score with AI (OpenRouter/Claude)
         ↓
Qualified Leads (Google Sheet)
```

**Time per run:** 10-15 minutes  
**Cost per run:** ~$3-4 (for 30 companies, 120 profiles)

---

## 🔧 What's Included

### Core System Files
- `main.py` - Main application
- `src/` - All core modules (6 files)
- `config.yaml` - Configuration settings
- `.env.example` - Environment variables template
- `requirements.txt` - Dependencies list

### Documentation (You're Reading One!)
- `README.md` - Technical documentation
- `SETUP_GUIDE.md` - Detailed setup instructions (comprehensive)
- `QUICKSTART.md` - Get started in 15 minutes
- `PROJECT_OVERVIEW.md` - Complete project overview
- `CLIENT_SUMMARY.md` - This document
- `DEPLOYMENT_CHECKLIST.md` - Production deployment checklist

### Utility Scripts
- `test_setup.py` - Test all connections
- `validate_config.py` - Show current configuration
- `create_icp_template.py` - Generate ICP template in Google Sheets
- `utils_clear_new_flags.py` - Reset "New Lead" flags

---

## 🚀 Getting Started

### Quick Path (15 minutes)
Follow **QUICKSTART.md** for step-by-step setup.

### Detailed Path (30 minutes)
Follow **SETUP_GUIDE.md** for comprehensive setup with explanations.

### What You Need
1. **Accounts:** Google, Apify, OpenRouter
2. **Money:** $15-25 initial credits (Apify + OpenRouter)
3. **Time:** 15-30 minutes for setup
4. **Skills:** Basic computer use (no coding needed)

---

## 💰 Cost Breakdown

### Per Run Costs
- **Apify (LinkedIn scraping):** ~$2.50-4.00
- **OpenRouter (AI scoring):** ~$0.10-0.20
- **Total:** ~$2.60-4.20 per run

### Monthly Estimates

| Frequency | Runs/Month | Cost |
|-----------|------------|------|
| Daily | 30 | ~$80-125 |
| Every 3 days | 10 | ~$25-40 |
| Weekly | 4 | ~$10-17 |
| Bi-weekly | 2 | ~$5-8 |

**Configurable limits let you control costs exactly.**

---

## ⚙️ Configuration (No Code!)

### ICP Settings (Google Sheet)
Edit these in your "ICP Settings" sheet - no code changes needed:

- **Industries:** Software, SaaS, Technology, etc.
- **Company Size:** Min/Max employees
- **Countries:** France, Belgium, Switzerland, etc.
- **Job Titles:** CEO, CTO, Founder, VP Sales, etc.
- **Keywords:** Required (B2B, Enterprise) and Excluded (Agency, Freelance)
- **Seniority:** C-Level, VP, Director, etc.
- **Departments:** Sales, Marketing, Operations, etc.
- **Company Types:** Startup, SMB, Enterprise
- **Languages:** French, English, etc.
- **Experience:** Min/Max years

**Change anytime. Next run uses new settings automatically.**

### Limits (config.yaml)
```yaml
limits:
  max_companies: 30              # How many companies to scrape
  max_profiles_per_company: 4    # How many profiles per company
```

**Adjust based on budget and needs.**

### Scoring (config.yaml)
```yaml
scoring:
  min_qualified_score: 60        # Minimum score to qualify (0-100)
```

**Higher = stricter, Lower = more leads.**

### Scheduling (config.yaml)
```yaml
scheduling:
  enabled: false                 # Set to true for auto-run
  interval_hours: 24             # How often to run
```

**Run manually or automatically.**

---

## 📈 Output Format

Your "Qualified Leads" Google Sheet will have:

| Column | Description |
|--------|-------------|
| Date Added | When lead was added |
| New Lead | YES/NO flag (know what's new!) |
| Lead Score | 0-100 score |
| Full Name | Contact name |
| Job Title | Their role |
| Company Name | Company |
| Company Size | Employee count |
| Industry | Industry |
| Location | City/Country |
| LinkedIn URL | Profile link (for outreach) |
| Email | If available |
| Phone | If available |
| Seniority Level | C-Level, VP, etc. |
| Department | Sales, Marketing, etc. |
| Years of Experience | If available |
| AI Reasoning | Why this score? |
| Profile Summary | Bio/summary |
| Company URL | Company LinkedIn |
| Last Updated | Timestamp |

**Ready for immediate outreach!**

---

## 🎯 How to Use

### First Time Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create ICP template
python create_icp_template.py

# 3. Edit your ICP in Google Sheet

# 4. Test setup
python test_setup.py

# 5. Small test run
python main.py --max-companies 2 --max-profiles 2
```

### Regular Use

#### Option 1: Manual Runs
```bash
# Run once with default settings
python main.py

# Or with custom limits
python main.py --max-companies 50 --max-profiles 5
```

#### Option 2: Automatic Scheduled Runs
```bash
# Runs continuously, every 24 hours
python main.py --schedule
```

### After Each Run
1. Open your "Qualified Leads" Google Sheet
2. Filter by "New Lead" = YES
3. Review leads and their scores
4. Reach out to qualified leads
5. Clear flags when done: `python utils_clear_new_flags.py`

---

## 🔍 Quality Control

### AI Scoring Dimensions
Each lead is scored across 5 dimensions:

1. **Job Title Match (30%)** - Does title match target roles?
2. **Company Fit (25%)** - Industry, size, location match?
3. **Seniority Level (20%)** - Right decision-maker level?
4. **Department Fit (15%)** - Department aligns with ICP?
5. **Keywords (10%)** - Required keywords present?

**Total score: 0-100**  
**Default threshold: 60** (configurable)

### AI Reasoning
Each lead includes explanation of the score:
- What matched well
- What didn't match
- Why the score was assigned

**Helps you prioritize outreach.**

---

## 🛠️ Maintenance

### Update ICP (Anytime)
1. Open "ICP Settings" Google Sheet
2. Edit Row 2 with new criteria
3. Save
4. Next run uses new ICP automatically

**No code changes. No redeployment. Just edit and go.**

### Adjust Limits
Edit `config.yaml` and change:
- `max_companies`
- `max_profiles_per_company`
- `min_qualified_score`
- `interval_hours`

### View Logs
```bash
# View recent activity
cat logs/sdr.log

# Follow in real-time
tail -f logs/sdr.log
```

---

## 🐛 Troubleshooting

### Common Issues

**"Permission Denied" on Google Sheets**
→ Share both sheets with service account email (from credentials.json)

**"No companies found"**
→ ICP too restrictive. Try broader criteria.

**"Insufficient credits" (Apify)**
→ Add more credits in Apify dashboard

**"Authentication failed" (OpenRouter)**
→ Check API key in .env file

**Low quality leads**
→ Adjust ICP settings or lower min_qualified_score

### Get Help
1. Check `logs/sdr.log`
2. Run `python test_setup.py`
3. Run `python validate_config.py`
4. Review `SETUP_GUIDE.md`
5. Check error message details

---

## 📚 Documentation Guide

**Where to start:**
- New user? → **QUICKSTART.md**
- Need details? → **SETUP_GUIDE.md**
- Technical info? → **README.md**
- Overview? → **PROJECT_OVERVIEW.md**
- Deploying? → **DEPLOYMENT_CHECKLIST.md**
- Quick ref? → This file!

**All documentation is in the project folder.**

---

## ✅ Success Checklist

After setup, you should see:

- [ ] System runs without errors
- [ ] Leads appear in "Qualified Leads" sheet
- [ ] Scores are reasonable (60-100 range)
- [ ] AI reasoning makes sense
- [ ] No duplicates
- [ ] New leads marked with YES
- [ ] Can change ICP without touching code
- [ ] LinkedIn URLs work for outreach

**If all checked: You're ready to generate leads!**

---

## 🎯 What Makes This System Special

### 1. Fully Configurable
- No hardcoded values
- Everything in config files or Google Sheets
- Change ICP without code changes
- Adjust limits on the fly

### 2. AI-Powered
- Claude 3.5 Sonnet scoring
- Detailed reasoning for each score
- Smart filtering
- Consistent evaluation

### 3. Production Ready
- Error handling
- Logging
- Duplicate prevention
- Rate limiting
- Retry logic

### 4. Cost Effective
- ~$3-4 per run
- Scalable limits
- Pay-as-you-go
- No subscriptions

### 5. Easy to Use
- Familiar interface (Google Sheets)
- No coding required
- Simple commands
- Clear documentation

---

## 📞 Next Steps

1. **Setup** → Follow QUICKSTART.md (15 min)
2. **Test** → Run with 2 companies first
3. **Refine** → Adjust ICP based on results
4. **Scale** → Increase limits gradually
5. **Automate** → Enable scheduling for continuous operation

---

## 🎁 Bonus Features

### Included Utilities
- **Setup validator** - Test all connections
- **Config validator** - Check settings
- **ICP template creator** - Auto-generate sheet structure
- **Flag clearer** - Reset new lead markers

### Smart Features
- **Duplicate detection** - Never adds same lead twice
- **New lead tracking** - Always know what's fresh
- **Seniority extraction** - Auto-detects from job titles
- **Department extraction** - Auto-categorizes
- **Company size parsing** - Handles ranges

---

## 💡 Pro Tips

1. **Start Small:** Test with 2-5 companies first
2. **Refine ICP:** Adjust based on first results
3. **Check Daily:** Review new leads regularly
4. **Use Filters:** Google Sheets filters are your friend
5. **Track Quality:** Note which criteria yield best leads
6. **Iterate:** Update ICP as you learn
7. **Monitor Costs:** Keep an eye on API usage
8. **Clear Flags:** Reset after reviewing leads

---

## 🚀 Ready to Launch?

```bash
# Test your setup
python test_setup.py

# Run your first test
python main.py --max-companies 2 --max-profiles 2

# Check your results
# Open "Qualified Leads" Google Sheet

# Happy with results? Go full scale!
python main.py
```

---

## 📊 Expected Results

After first full run (30 companies, 4 profiles each):
- **Profiles scraped:** ~120
- **Qualified leads:** ~30-50 (depends on ICP strictness)
- **Time:** ~15 minutes
- **Cost:** ~$3-4

**Quality over quantity. AI filters out poor fits automatically.**

---

## 🎉 That's It!

You now have a fully automated lead generation system that:

✅ Never forgets to search for leads  
✅ Always applies the same criteria  
✅ Scores objectively with AI  
✅ Saves you hours of manual work  
✅ Continuously finds new opportunities  
✅ Costs ~$3-4 per run  

**Start generating leads today! Follow QUICKSTART.md to begin.**

---

## Questions?

- Setup issues? → See **SETUP_GUIDE.md**
- Need details? → See **PROJECT_OVERVIEW.md**
- Technical info? → See **README.md**
- Errors? → Check **logs/sdr.log**

**All documentation is self-contained in the project folder.**

Good luck with your lead generation! 🎯🚀
