# ✅ Setup Checklist - Before Running Docker

## 📋 Required Files (You Need to Create These)

Before running `docker-compose up`, make sure you have:

### ☐ **1. `.env` file** (in project root)

Create a file named `.env` with your actual credentials:

```bash
# Copy this template and replace with YOUR values:

APIFY_API_TOKEN=your_actual_apify_token
OPENROUTER_API_KEY=your_actual_openrouter_key
ICP_SHEET_ID=your_google_sheet_id_for_icp
OUTPUT_SHEET_ID=your_google_sheet_id_for_output
```

**Where to get these:**
- Apify Token: https://console.apify.com/account/integrations
- OpenRouter Key: https://openrouter.ai/keys
- Sheet IDs: From your Google Sheets URL (the long string after `/d/`)

---

### ☐ **2. `credentials.json` file** (in project root)

Your Google Service Account JSON file.

**How to get it:**
1. Go to: https://console.cloud.google.com/
2. Create a service account (or use existing)
3. Download the JSON key file
4. Rename it to `credentials.json`
5. Place in project root folder

**File should look like:**
```json
{
  "type": "service_account",
  "project_id": "your-project-12345",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "123456789",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token"
}
```

**⚠️ IMPORTANT:** Share your Google Sheets with this service account email!

---

### ☐ **3. Docker Desktop Installed**

Download from: https://www.docker.com/products/docker-desktop/

---

## 🚀 Ready to Run?

Once you have all 3 items above:

```bash
cd SDR
docker-compose up
```

---

## 📂 Your Project Structure Should Look Like:

```
SDR/
├── .env                    ← YOU CREATE THIS
├── credentials.json        ← YOU CREATE THIS
├── Dockerfile              ✓ Already included
├── docker-compose.yml      ✓ Already included
├── main.py                 ✓ Already included
├── requirements.txt        ✓ Already included
└── ...
```

---

## 🆘 Troubleshooting

### "FileNotFoundError: credentials.json"
→ Make sure `credentials.json` is in the project root (same folder as Dockerfile)

### "APIFY_API_TOKEN not found"
→ Check your `.env` file exists and has correct variable names

### "Permission denied" (Google Sheets)
→ Share your sheets with the service account email from credentials.json

---

## 💡 Quick Test

To verify your setup BEFORE running Docker:

```bash
# Check files exist:
ls .env credentials.json

# Check .env has content:
cat .env

# Check credentials.json has content:
cat credentials.json
```

All files present? Great! Run: `docker-compose up`

---

**Need detailed help?** See [DOCKER_SETUP.md](DOCKER_SETUP.md) for complete instructions.
