# AI SDR - Deployment Checklist

Use this checklist to ensure everything is properly set up before running in production.

---

## Pre-Deployment

### ☐ 1. Accounts Created
- [ ] Google Cloud account created
- [ ] Apify account created and verified
- [ ] OpenRouter account created
- [ ] Credit added to Apify (~$10-20)
- [ ] Credit added to OpenRouter (~$5-10)

### ☐ 2. Google Sheets Setup
- [ ] "AI SDR - ICP Settings" sheet created
- [ ] "AI SDR - Qualified Leads" sheet created
- [ ] Both sheet IDs copied and saved
- [ ] Google Cloud project created
- [ ] Google Sheets API enabled
- [ ] Google Drive API enabled
- [ ] Service account created
- [ ] Service account JSON key downloaded as `credentials.json`
- [ ] Both sheets shared with service account email (Editor permissions)

### ☐ 3. API Keys Obtained
- [ ] Apify API token copied
- [ ] OpenRouter API key copied
- [ ] Both keys tested and valid

### ☐ 4. Project Setup
- [ ] Python 3.9+ installed
- [ ] Project downloaded/cloned
- [ ] Virtual environment created (recommended)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `credentials.json` in project root
- [ ] `.env` file created from `.env.example`
- [ ] All values in `.env` filled in

---

## Configuration

### ☐ 5. Environment Variables (.env)
```
- [ ] APIFY_API_TOKEN set
- [ ] OPENROUTER_API_KEY set
- [ ] GOOGLE_SHEETS_CREDENTIALS_PATH set (should be: credentials.json)
- [ ] ICP_SHEET_ID set (from Google Sheet URL)
- [ ] OUTPUT_SHEET_ID set (from Google Sheet URL)
- [ ] ICP_SHEET_TAB_NAME set (default: "ICP Settings")
- [ ] OUTPUT_SHEET_TAB_NAME set (default: "Qualified Leads")
- [ ] APIFY_COMPANY_SCRAPER_ACTOR set
- [ ] APIFY_EMPLOYEE_SCRAPER_ACTOR set
```

### ☐ 6. Configuration File (config.yaml)
```
- [ ] max_companies set (recommended start: 30)
- [ ] max_profiles_per_company set (recommended: 4)
- [ ] scheduling.enabled set (false for manual, true for auto)
- [ ] scheduling.interval_hours set (if using scheduling)
- [ ] min_qualified_score set (recommended: 60)
- [ ] openrouter.model confirmed (default: anthropic/claude-3.5-sonnet)
- [ ] logging.level set (INFO for production)
```

### ☐ 7. ICP Settings (Google Sheet)
- [ ] ICP template created (`python create_icp_template.py`)
- [ ] Row 2 filled with your ICP criteria:
  - [ ] Industries
  - [ ] Company Size Min/Max
  - [ ] Countries
  - [ ] Target Job Titles
  - [ ] Required Keywords (if any)
  - [ ] Seniority Levels
  - [ ] Departments
  - [ ] Company Types
  - [ ] Languages
  - [ ] Excluded Keywords (if any)
  - [ ] Years Experience Min/Max (if needed)

---

## Testing

### ☐ 8. Setup Validation
```bash
- [ ] Run: python test_setup.py
- [ ] All tests pass (✓)
- [ ] No errors in output
```

### ☐ 9. Configuration Validation
```bash
- [ ] Run: python validate_config.py
- [ ] All settings shown correctly
- [ ] No "NOT SET" values
- [ ] Credentials file exists
```

### ☐ 10. Small Test Run
```bash
- [ ] Run: python main.py --max-companies 2 --max-profiles 2
- [ ] Script completes without errors
- [ ] Logs show successful execution (check logs/sdr.log)
- [ ] Google Sheet has new entries
- [ ] Entries marked with "New Lead" = YES
- [ ] Scores are reasonable (0-100)
- [ ] AI reasoning makes sense
```

### ☐ 11. Results Verification
- [ ] Open "AI SDR - Qualified Leads" sheet
- [ ] Check all columns are populated
- [ ] LinkedIn URLs are valid
- [ ] Company information is accurate
- [ ] Lead scores match expectations
- [ ] No duplicate entries

---

## First Production Run

### ☐ 12. Pre-Flight Check
```bash
- [ ] Test run completed successfully
- [ ] ICP settings finalized
- [ ] Limits confirmed (max_companies, max_profiles)
- [ ] Minimum score threshold confirmed
- [ ] Sufficient credits in Apify (~$4 per run)
- [ ] Sufficient credits in OpenRouter (~$0.20 per run)
```

### ☐ 13. Execute Production Run
```bash
- [ ] Run: python main.py
- [ ] Monitor progress in terminal
- [ ] Check logs/sdr.log for any warnings
- [ ] Wait for completion (10-15 minutes)
```

### ☐ 14. Post-Run Validation
- [ ] Check terminal output for summary:
  - [ ] Companies scraped count
  - [ ] Profiles scraped count
  - [ ] Qualified leads count
  - [ ] New leads added count
- [ ] Open Google Sheet
- [ ] Verify new leads are present
- [ ] Spot-check lead quality
- [ ] Review AI reasoning for sample leads
- [ ] Check for any duplicate entries (should be none)

---

## Scheduling (Optional)

### ☐ 15. Schedule Configuration
If running on schedule:
```yaml
- [ ] config.yaml: scheduling.enabled set to true
- [ ] config.yaml: scheduling.interval_hours set (default: 24)
- [ ] Decided when to run (time of day)
```

### ☐ 16. Launch Scheduled Job
```bash
- [ ] Run: python main.py --schedule
- [ ] Verify immediate first run starts
- [ ] Check logs show "Running in scheduled mode"
- [ ] Let it run in background or use a process manager
```

### ☐ 17. Process Management (Production)
For 24/7 operation, consider:
- [ ] Screen/tmux session (Linux/Mac)
- [ ] Windows Task Scheduler (Windows)
- [ ] Docker container
- [ ] Systemd service (Linux)
- [ ] Cloud VM with autostart

---

## Monitoring & Maintenance

### ☐ 18. Setup Monitoring
- [ ] Bookmark Google Sheets URLs
- [ ] Set up log monitoring (logs/sdr.log)
- [ ] Create calendar reminder to check leads (daily/weekly)
- [ ] Monitor Apify credit balance
- [ ] Monitor OpenRouter credit balance

### ☐ 19. Regular Checks
Weekly:
- [ ] Review new leads in Google Sheet
- [ ] Clear "New Lead" flags after review (`python utils_clear_new_flags.py`)
- [ ] Check logs for any errors
- [ ] Verify no duplicates appearing

Monthly:
- [ ] Review lead quality
- [ ] Adjust ICP if needed
- [ ] Adjust min_qualified_score if needed
- [ ] Check API credit usage
- [ ] Review cost vs. results

### ☐ 20. Troubleshooting Resources
- [ ] SETUP_GUIDE.md bookmarked
- [ ] test_setup.py location known
- [ ] validate_config.py location known
- [ ] Know how to read logs/sdr.log
- [ ] Contact info for support (if applicable)

---

## Production Best Practices

### ☐ 21. Backup & Security
- [ ] Backup credentials.json securely
- [ ] Keep .env file secure (never commit to git)
- [ ] Document all API keys in secure location
- [ ] Save Google Sheet IDs somewhere safe

### ☐ 22. Cost Management
- [ ] Set budget alerts in Apify
- [ ] Monitor OpenRouter usage
- [ ] Calculate monthly costs based on frequency
- [ ] Adjust limits if costs are too high

### ☐ 23. Quality Assurance
- [ ] First 10 leads reviewed for quality
- [ ] ICP settings tuned if needed
- [ ] Scoring threshold adjusted if needed
- [ ] Excluded keywords added if needed

---

## Optimization (After First Week)

### ☐ 24. Performance Review
After ~5-10 runs, review:
- [ ] What percentage of leads are high quality?
- [ ] Are scores accurate?
- [ ] Any patterns in low-quality leads?
- [ ] Any common companies/profiles to exclude?

### ☐ 25. ICP Refinement
Based on results:
- [ ] Update Industries (add/remove)
- [ ] Adjust Company Size range
- [ ] Refine Target Job Titles
- [ ] Add Required Keywords
- [ ] Add Excluded Keywords
- [ ] Adjust Seniority Levels
- [ ] Update Countries if needed

### ☐ 26. Scaling Decisions
- [ ] Increase max_companies if results are good
- [ ] Increase max_profiles_per_company if needed
- [ ] Adjust frequency (more/less often)
- [ ] Consider multiple ICP profiles

---

## Sign-Off

### ☐ 27. Final Checklist
- [ ] System runs without errors
- [ ] Leads appear in Google Sheets
- [ ] Lead quality is acceptable
- [ ] No duplicates
- [ ] New lead tracking works
- [ ] Costs are within budget
- [ ] Can modify ICP without code changes
- [ ] Documentation is accessible
- [ ] Backup of all credentials made

### ☐ 28. Deployment Complete
```
Deployed by: _______________________
Date: _______________________
First run results: _______ companies, _______ profiles, _______ qualified leads
Sign-off: _______________________
```

---

## Emergency Contacts

```
Apify Support: https://apify.com/support
OpenRouter Support: https://openrouter.ai/
Google Cloud Support: https://cloud.google.com/support

Developer/Support Contact: _______________________
```

---

## Quick Commands Reference

```bash
# Test setup
python test_setup.py

# Validate configuration
python validate_config.py

# Create ICP template
python create_icp_template.py

# Test run (2 companies, 2 profiles each)
python main.py --max-companies 2 --max-profiles 2

# Full production run
python main.py

# Scheduled run (continuous)
python main.py --schedule

# Custom limits
python main.py --max-companies 50 --max-profiles 5

# Clear new lead flags
python utils_clear_new_flags.py

# View logs
tail -f logs/sdr.log  # Mac/Linux
type logs\sdr.log     # Windows
```

---

**✅ Checklist Complete = Ready for Production**

Good luck with your lead generation! 🎯
