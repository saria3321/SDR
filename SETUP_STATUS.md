# ✅ Setup Status - Ready to Test!

## Current Status: Configured & Ready

Your credentials have been configured successfully!

---

## ✅ What's Done

1. **Environment Variables (.env)** - Configured
   - Apify API Token: Set
   - OpenRouter API Key: Set
   - Google Sheets IDs: Set
   - Actor IDs: Set to `harvestapi/linkedin-profile-search`

2. **Google Credentials** - Configured
   - Project: hyvop-481511
   - Service Account: hyvop-ai-automation@hyvop-481511.iam.gserviceaccount.com

3. **Google Sheets**
   - ICP Sheet: https://docs.google.com/spreadsheets/d/1Z1N2p8t0iUB2FaldGcpDGsu7qbbKTJ-LfB6PQKn7v3Y
   - Output Sheet: https://docs.google.com/spreadsheets/d/1wIzjo9vJfAZiutLxeSv_0zqGviGwFFrK7DkP3lSrUxc

---

## ⚠️ Important: Share Google Sheets

**YOU MUST DO THIS:**

Go to both Google Sheets and share with:
```
hyvop-ai-automation@hyvop-481511.iam.gserviceaccount.com
```

Give **Editor** permissions.

---

## 🚀 Next Steps

### Step 1: Install Dependencies

```bash
pip install google-auth google-auth-oauthlib google-api-python-client gspread apify-client python-dotenv pyyaml requests schedule pydantic
```

### Step 2: Share Google Sheets

1. Open ICP Sheet: https://docs.google.com/spreadsheets/d/1Z1N2p8t0iUB2FaldGcpDGsu7qbbKTJ-LfB6PQKn7v3Y
2. Click "Share"
3. Add: `hyvop-ai-automation@hyvop-481511.iam.gserviceaccount.com`
4. Give "Editor" access
5. Repeat for Output Sheet: https://docs.google.com/spreadsheets/d/1wIzjo9vJfAZiutLxeSv_0zqGviGwFFrK7DkP3lSrUxc

### Step 3: Setup ICP Sheet

In your ICP Sheet (first one):
1. Create tab named "ICP Settings"
2. Row 1: Add headers
3. Row 2: Add your ICP data

**Headers needed:**
- Industries
- Company Size Min
- Company Size Max
- Countries  
- Target Job Titles
- Required Keywords
- Seniority Levels
- Departments
- Company Types
- Languages
- Excluded Keywords
- Years Experience Min
- Years Experience Max

### Step 4: Run Tests

```bash
# Test Apify
python test_apify_actor.py

# Small test (4 profiles)
python main_simplified.py --max-companies 2 --max-profiles 2
```

### Step 5: Check Results

Open Output Sheet - you should see qualified leads!

---

## 📊 Expected Cost (Test Run)

- Apify: ~$0.10 (4 profiles)
- OpenRouter: ~$0.02 (4 profiles)
- **Total: ~$0.12 for test**

---

## 🐛 If You Get Errors

### "Permission Denied" (Google Sheets)
→ Share sheets with service account email (see above)

### "Insufficient credits" (Apify)
→ Add $5-10 to Apify account

### "Module not found"
→ Install dependencies (see Step 1)

---

## 📞 System is Ready!

Everything is configured. Just need to:
1. Install Python dependencies
2. Share Google Sheets
3. Set up ICP in sheet
4. Run test!

---

**Questions? Check README.md or run `python simple_test.py`**
