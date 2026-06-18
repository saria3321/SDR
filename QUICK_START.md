# 🚀 AI SDR - Quick Start Guide

## Choose Your Setup Method

### 🐳 **Docker Setup (Recommended - Easiest)**
Perfect if you want to avoid Python/dependency issues.

👉 **[See DOCKER_SETUP.md](DOCKER_SETUP.md)**

```bash
# 1. Install Docker Desktop
# 2. Create .env file with your API keys
# 3. Add credentials.json file
# 4. Run:
docker-compose up
```

---

### 💻 **Local Python Setup**
If you prefer running directly on your machine.

#### Requirements:
- Python 3.7 or higher
- pip

#### Steps:

1. **Clone/Download the project**
   ```bash
   cd SDR
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `.env` file** with your credentials:
   ```
   APIFY_API_TOKEN=your_token
   OPENROUTER_API_KEY=your_key
   ICP_SHEET_ID=your_sheet_id
   OUTPUT_SHEET_ID=your_sheet_id
   ```

4. **Add `credentials.json`** (Google Service Account)

5. **Run:**
   ```bash
   # Test run (6 leads)
   python main.py --max-companies 2 --max-profiles 3

   # Full run (120 leads)
   python main.py
   ```

---

## 📋 What You Need

### 1. Apify API Token
- Get from: https://console.apify.com/account/integrations
- Free tier: $5 credits

### 2. OpenRouter API Key  
- Get from: https://openrouter.ai/keys
- Pay-as-you-go pricing

### 3. Google Service Account
- Create at: https://console.cloud.google.com/
- Enable Google Sheets API
- Download JSON credentials
- Share your Google Sheets with the service account email

### 4. Google Sheets
- **ICP Settings Sheet**: Your target criteria (industries, countries, job titles)
- **Output Sheet**: Where leads will be written

---

## 🎯 Expected Output

After running, you'll get qualified leads in your Google Sheet with:
- ✅ Full name, job title, company
- ✅ LinkedIn profile URL
- ✅ Location, industry, company size
- ✅ AI score & reasoning
- ✅ Ready for outreach!

---

## 💰 Costs

Per 120 leads generated:
- Apify: ~$0.40
- OpenRouter AI: ~$0.10-0.20
- **Total: ~$0.50-0.70**

---

## 🆘 Need Help?

- 🐳 Docker issues → [DOCKER_SETUP.md](DOCKER_SETUP.md)
- 🔧 Configuration → [CLIENT_MESSAGE.md](CLIENT_MESSAGE.md)
- 🐛 Troubleshooting → Check `logs/sdr.log`

---

**Choose Docker if you want the easiest setup! 🐳**
