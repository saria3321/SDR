# 🐳 AI SDR - Docker Setup Guide

## Quick Start (3 Steps)

### Step 1: Install Docker
- **Windows/Mac**: Download [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Linux**: 
  ```bash
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  ```

### Step 2: Setup Configuration Files

1. **Create `.env` file** in the project root:
   ```bash
   APIFY_API_TOKEN=your_apify_token_here
   OPENROUTER_API_KEY=your_openrouter_key_here
   ICP_SHEET_ID=your_icp_sheet_id
   OUTPUT_SHEET_ID=your_output_sheet_id
   ```

2. **Add `credentials.json`** (Google Service Account):
   - Download from Google Cloud Console
   - Place in project root folder
   - File should look like:
     ```json
     {
       "type": "service_account",
       "project_id": "your-project",
       "private_key_id": "...",
       "private_key": "-----BEGIN PRIVATE KEY-----\n...",
       "client_email": "your-service-account@project.iam.gserviceaccount.com"
     }
     ```

### Step 3: Run the Application

**Option A: Using Docker Compose (Recommended)**
```bash
# Navigate to project directory
cd /path/to/SDR

# Build and run
docker-compose up
```

**Option B: Using Docker directly**
```bash
# Build image
docker build -t ai-sdr .

# Run container
docker run --env-file .env -v $(pwd)/credentials.json:/app/credentials.json ai-sdr
```

---

## ⚙️ Custom Runs

### Run with custom parameters:
```bash
# Generate 20 leads (10 companies × 2 profiles)
docker run --env-file .env \
  -v $(pwd)/credentials.json:/app/credentials.json \
  ai-sdr \
  python main.py --max-companies 10 --max-profiles 2
```

### Run full pipeline (120 leads):
```bash
docker-compose run ai-sdr python main.py
```

### Run test (6 leads):
```bash
docker-compose run ai-sdr python main.py --max-companies 2 --max-profiles 3
```

---

## 📊 View Results

While running, check:
- **Google Sheets**: Your qualified leads appear in real-time
- **Logs**: `./logs/sdr.log` (mounted from container)

---

## 🔧 Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### "credentials.json not found"
- Make sure file exists in project root
- Check file permissions (should be readable)

### "Permission denied" on Linux
```bash
# Add your user to docker group
sudo usermod -aG docker $USER
# Log out and back in
```

### API errors (401/403)
- Verify `.env` file has correct API tokens
- Check Apify credits: https://console.apify.com/
- Check OpenRouter credits: https://openrouter.ai/

---

## 🎯 What This Does

1. ✅ Scrapes LinkedIn companies matching your ICP
2. ✅ Finds decision-makers at those companies
3. ✅ Scores leads with AI
4. ✅ Writes qualified leads to Google Sheets
5. ✅ **No LinkedIn cookies needed!**

---

## 📦 Project Structure
```
SDR/
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Docker Compose configuration
├── .env                       # Your API keys (CREATE THIS)
├── credentials.json           # Google credentials (CREATE THIS)
├── main.py                    # Main application
├── config.yaml                # Settings
├── requirements.txt           # Python dependencies
└── logs/                      # Application logs
```

---

## 🚀 Production Deployment

### Run in background (detached mode):
```bash
docker-compose up -d
```

### View logs:
```bash
docker-compose logs -f
```

### Stop:
```bash
docker-compose down
```

### Auto-restart on failure:
Already configured in `docker-compose.yml` with `restart: unless-stopped`

---

## 💰 Expected Costs

Per 120 leads:
- Apify: ~$0.40-0.50
- OpenRouter: ~$0.10-0.20
- **Total: ~$0.50-0.70**

---

## ✅ Success Indicators

When running correctly, you'll see:
```
[Step 1/5] Loading ICP Settings from Google Sheets
[Step 2/5] Scraping LinkedIn Data via Apify
Found 30 companies
[Step 3/5] Scoring Leads with AI (OpenRouter)
[Step 4/5] Writing to Google Sheets
[Step 5/5] Pipeline Summary
Pipeline completed successfully!
```

---

## 📞 Support

If you encounter issues:
1. Check logs: `docker-compose logs`
2. Verify all credentials are correct
3. Test with small run first: `--max-companies 1 --max-profiles 2`

---

**That's it! Your AI SDR system is now running in Docker.** 🎉
