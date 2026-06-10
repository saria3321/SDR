# 🚀 Quick Start - Generate Your First Leads!

## Step 1: Open Google Colab Notebook

Click this link (opens in new tab):
**https://colab.research.google.com/github/saria3321/SDR/blob/main/AI_SDR_Google_Colab.ipynb**

## Step 2: Add Your Credentials

Find **Step 3** in the notebook and replace:

```python
APIFY_API_TOKEN = "YOUR_APIFY_TOKEN_HERE"
OPENROUTER_API_KEY = "YOUR_OPENROUTER_KEY_HERE"
ICP_SHEET_ID = "YOUR_ICP_SHEET_ID"
OUTPUT_SHEET_ID = "YOUR_OUTPUT_SHEET_ID"
```

AND replace the `credentials` JSON with your actual Google Service Account JSON (from credentials.json file).

## Step 3: Run It!

1. Click: **Runtime** → **Run all**
2. Wait 5-10 minutes
3. Check your **Qualified Leads** sheet - it will be filled with leads!

## What Will Happen:

1. ✅ Installs Python packages (2 min)
2. ✅ Downloads code from GitHub (30 sec)
3. ✅ Searches LinkedIn for matching profiles (5-8 min)
4. ✅ Scores each profile with AI (2-3 min)
5. ✅ Saves to your Google Sheet

## Expected Output:

Your **Qualified Leads** sheet will show:
- Full Name
- Job Title  
- Company Name
- LinkedIn URL (for outreach!)
- AI Score (0-100)
- AI Reasoning
- Industry, Location, Size
- And 10+ more fields

## Cost for Test Run:
- 4 profiles (2 companies × 2 profiles)
- **~$0.10 total**

---

## Option 2: Run Locally (If You Prefer)

```bash
cd e:/fiverr/SDR
python main_simplified.py --max-companies 2 --max-profiles 2
```

This will do the same thing but from your computer instead of Google Colab.

---

**Need help? Let me know!** 🚀
