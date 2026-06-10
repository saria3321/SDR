# AI SDR - System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                               │
│                                                                       │
│  ┌────────────────────────┐         ┌─────────────────────────┐    │
│  │  ICP Settings Sheet    │         │  Qualified Leads Sheet  │    │
│  │  (Input Configuration) │         │  (Output Results)       │    │
│  └───────────┬────────────┘         └─────────────▲───────────┘    │
│              │                                     │                 │
└──────────────┼─────────────────────────────────────┼────────────────┘
               │                                     │
               │                                     │
┌──────────────▼─────────────────────────────────────┼────────────────┐
│                      AI SDR SYSTEM                  │                │
│                                                     │                │
│  ┌──────────────┐    ┌──────────────┐    ┌────────┴──────┐        │
│  │ ICP Loader   │───▶│   Scraper    │───▶│  AI Scorer    │        │
│  │              │    │              │    │               │        │
│  │ - Reads ICP  │    │ - Companies  │    │ - Score 0-100 │        │
│  │ - Validates  │    │ - Employees  │    │ - Reasoning   │        │
│  └──────────────┘    └──────┬───────┘    └───────┬───────┘        │
│                              │                    │                 │
│                              │                    │                 │
│  ┌──────────────────────────▼────────────────────▼──────────────┐ │
│  │                   Sheets Writer                               │ │
│  │  - Duplicate detection                                        │ │
│  │  - New lead marking                                           │ │
│  │  - Append to sheet                                            │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
               │                    │                    │
               │                    │                    │
┌──────────────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Google Sheets API    │  │   Apify API     │  │  OpenRouter API │
│  (Read/Write)         │  │   (Scraping)    │  │  (AI Scoring)   │
└───────────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         main.py                                  │
│                    (Entry Point)                                 │
│                                                                   │
│  - Parse arguments                                               │
│  - Load configuration                                            │
│  - Setup logging                                                 │
│  - Orchestrate pipeline                                          │
│  - Handle scheduling                                             │
└───────────────────────────┬─────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌──────▼──────┐  ┌────────▼────────┐
│  config.yaml   │  │    .env     │  │  credentials.json│
│  (Settings)    │  │  (Secrets)  │  │  (Google Auth)   │
└────────────────┘  └─────────────┘  └──────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│                         src/ Modules                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐         ┌─────────────────────┐          │
│  │    models.py     │◄────────│   All Modules       │          │
│  │                  │         │   (Use Models)      │          │
│  │ - ICPSettings    │         └─────────────────────┘          │
│  │ - CompanyProfile │                                           │
│  │ - EmployeeProfile│                                           │
│  │ - ScoredLead     │                                           │
│  └──────────────────┘                                           │
│                                                                   │
│  ┌──────────────────────────────────────────────┐               │
│  │              icp_loader.py                   │               │
│  │  ┌─────────────────────────────────────┐    │               │
│  │  │ 1. Connect to Google Sheets         │    │               │
│  │  │ 2. Read ICP Settings sheet          │    │               │
│  │  │ 3. Parse and validate criteria      │    │               │
│  │  │ 4. Return ICPSettings object        │    │               │
│  │  └─────────────────────────────────────┘    │               │
│  └──────────────────────────────────────────────┘               │
│                                                                   │
│  ┌──────────────────────────────────────────────┐               │
│  │            apify_scraper.py                  │               │
│  │  ┌─────────────────────────────────────┐    │               │
│  │  │ 1. Build search query from ICP      │    │               │
│  │  │ 2. Find companies (Apify actor 1)   │    │               │
│  │  │ 3. For each company:                │    │               │
│  │  │    - Extract employees (actor 2)    │    │               │
│  │  │    - Parse profile data             │    │               │
│  │  │    - Rate limit between requests    │    │               │
│  │  │ 4. Return all EmployeeProfile[]     │    │               │
│  │  └─────────────────────────────────────┘    │               │
│  └──────────────────────────────────────────────┘               │
│                                                                   │
│  ┌──────────────────────────────────────────────┐               │
│  │              ai_scorer.py                    │               │
│  │  ┌─────────────────────────────────────┐    │               │
│  │  │ 1. Build scoring prompt             │    │               │
│  │  │ 2. Include profile + ICP details    │    │               │
│  │  │ 3. Call OpenRouter API              │    │               │
│  │  │ 4. Parse score (0-100) & reasoning  │    │               │
│  │  │ 5. Filter by min_qualified_score    │    │               │
│  │  │ 6. Return ScoredLead[]              │    │               │
│  │  └─────────────────────────────────────┘    │               │
│  └──────────────────────────────────────────────┘               │
│                                                                   │
│  ┌──────────────────────────────────────────────┐               │
│  │            sheets_writer.py                  │               │
│  │  ┌─────────────────────────────────────┐    │               │
│  │  │ 1. Connect to output sheet          │    │               │
│  │  │ 2. Get existing LinkedIn URLs       │    │               │
│  │  │ 3. Check for duplicates             │    │               │
│  │  │ 4. Prepare new rows                 │    │               │
│  │  │ 5. Append to sheet                  │    │               │
│  │  │ 6. Mark as "New Lead" = YES         │    │               │
│  │  │ 7. Update old leads to NO           │    │               │
│  │  └─────────────────────────────────────┘    │               │
│  └──────────────────────────────────────────────┘               │
│                                                                   │
│  ┌──────────────────────────────────────────────┐               │
│  │              scheduler.py                    │               │
│  │  ┌─────────────────────────────────────┐    │               │
│  │  │ 1. Schedule job at interval         │    │               │
│  │  │ 2. Run immediately (first time)     │    │               │
│  │  │ 3. Wait for next scheduled time     │    │               │
│  │  │ 4. Repeat continuously              │    │               │
│  │  └─────────────────────────────────────┘    │               │
│  └──────────────────────────────────────────────┘               │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
START
  │
  ├─[Load Configuration]
  │   ├─ config.yaml
  │   ├─ .env
  │   └─ credentials.json
  │
  ├─[Step 1: Load ICP]
  │   │
  │   ├─ icp_loader.py
  │   │   └─ Connect to Google Sheets
  │   │       └─ Read "ICP Settings" sheet
  │   │           └─ Parse criteria
  │   │               └─ Return ICPSettings
  │   │
  │   └─ ICPSettings {
  │         industries: [...]
  │         job_titles: [...]
  │         countries: [...]
  │         ...
  │       }
  │
  ├─[Step 2: Scrape Companies]
  │   │
  │   ├─ apify_scraper.py
  │   │   └─ Build LinkedIn search query
  │   │       └─ Call Apify Company Scraper
  │   │           └─ Parse results
  │   │               └─ Return CompanyProfile[]
  │   │
  │   └─ [Company 1, Company 2, ..., Company 30]
  │
  ├─[Step 3: Scrape Employees]
  │   │
  │   ├─ For each Company:
  │   │   └─ apify_scraper.py
  │   │       └─ Call Apify Employee Scraper
  │   │           └─ Filter by job titles
  │   │               └─ Parse profiles
  │   │                   └─ Add to EmployeeProfile[]
  │   │
  │   └─ [Profile 1, Profile 2, ..., Profile 120]
  │
  ├─[Step 4: Score Leads]
  │   │
  │   ├─ For each EmployeeProfile:
  │   │   └─ ai_scorer.py
  │   │       └─ Build scoring prompt
  │   │           └─ Call OpenRouter API
  │   │               └─ Parse score & reasoning
  │   │                   └─ Create ScoredLead
  │   │
  │   ├─ Filter by min_qualified_score (≥60)
  │   │
  │   └─ [Scored Lead 1 (75), Lead 2 (82), ..., Lead N (65)]
  │
  ├─[Step 5: Write to Sheet]
  │   │
  │   ├─ sheets_writer.py
  │   │   ├─ Get existing LinkedIn URLs
  │   │   ├─ Filter out duplicates
  │   │   ├─ Prepare new rows
  │   │   ├─ Append to "Qualified Leads" sheet
  │   │   └─ Mark as "New Lead" = YES
  │   │
  │   └─ Google Sheets updated
  │
  └─[DONE]
      │
      └─ Summary logged:
          - Companies scraped: 30
          - Profiles scraped: 120
          - Qualified leads: 45
          - New leads added: 38
          - Duplicates skipped: 7
```

---

## Module Dependencies

```
main.py
  ├─→ src.icp_loader (ICPLoader)
  ├─→ src.apify_scraper (ApifyScraper)
  ├─→ src.ai_scorer (AIScorer)
  ├─→ src.sheets_writer (SheetsWriter)
  └─→ src.scheduler (JobScheduler)

src.icp_loader
  ├─→ src.models (ICPSettings)
  ├─→ gspread
  └─→ google.oauth2

src.apify_scraper
  ├─→ src.models (ICPSettings, CompanyProfile, EmployeeProfile)
  └─→ apify_client

src.ai_scorer
  ├─→ src.models (ICPSettings, EmployeeProfile, ScoredLead)
  └─→ openai (OpenRouter)

src.sheets_writer
  ├─→ src.models (ScoredLead)
  ├─→ gspread
  └─→ google.oauth2

src.scheduler
  └─→ schedule

src.models
  └─→ pydantic
```

---

## API Integration Points

```
┌──────────────────────┐
│   Google Sheets API  │
│                      │
│  Endpoints Used:     │
│  - spreadsheets.get  │
│  - spreadsheets.values.get │
│  - spreadsheets.values.update │
│  - spreadsheets.values.append │
│                      │
│  Authentication:     │
│  - Service Account   │
│  - OAuth2            │
│                      │
│  Rate Limits:        │
│  - 100 requests/100s │
│  - Well within limit │
└──────────────────────┘

┌──────────────────────┐
│     Apify API        │
│                      │
│  Actors Used:        │
│  1. Company Scraper  │
│     - Input: search  │
│     - Output: cos[]  │
│                      │
│  2. Employee Scraper │
│     - Input: co URL  │
│     - Output: emps[] │
│                      │
│  Authentication:     │
│  - API Token         │
│                      │
│  Cost Model:         │
│  - Credit-based      │
│  - ~$3-4 per run     │
└──────────────────────┘

┌──────────────────────┐
│   OpenRouter API     │
│                      │
│  Model:              │
│  - claude-3.5-sonnet │
│                      │
│  Endpoint:           │
│  - /chat/completions │
│                      │
│  Input:              │
│  - System prompt     │
│  - User prompt (ICP) │
│                      │
│  Output:             │
│  - Score: 0-100      │
│  - Reasoning: text   │
│                      │
│  Authentication:     │
│  - API Key           │
│                      │
│  Cost:               │
│  - ~$0.10-0.20/run   │
└──────────────────────┘
```

---

## Error Handling Flow

```
┌─────────────────────┐
│   Try Operation     │
└──────────┬──────────┘
           │
           ├─ Success ──────────────────────────────┐
           │                                         │
           ├─ API Error                             │
           │   ├─ Rate Limit ──→ Wait & Retry       │
           │   ├─ Auth Error ──→ Log & Fail         │
           │   └─ Timeout ───→ Retry (max 3)        │
           │                                         │
           ├─ Data Error                            │
           │   ├─ Parse Error ──→ Skip & Log        │
           │   ├─ Validation ───→ Skip & Log        │
           │   └─ Missing Data ─→ Use Default       │
           │                                         │
           └─ System Error                          │
               ├─ Network ────→ Retry               │
               ├─ Disk Full ──→ Log & Fail          │
               └─ Unknown ────→ Log & Continue      │
                                                     │
                                                     ▼
                                              ┌─────────────┐
                                              │   Success   │
                                              │  Continue   │
                                              └─────────────┘
```

---

## Logging Architecture

```
┌────────────────────────────────────────────┐
│              Logging System                 │
├────────────────────────────────────────────┤
│                                             │
│  Level: INFO (production)                   │
│  Output: logs/sdr.log + console            │
│                                             │
│  Format:                                    │
│  [Timestamp] [Module] [Level] Message      │
│                                             │
│  Example:                                   │
│  2024-06-09 10:15:23 - icp_loader - INFO  │
│  Loaded ICP: 3 industries, 5 titles       │
│                                             │
├────────────────────────────────────────────┤
│             Log Categories                  │
├────────────────────────────────────────────┤
│                                             │
│  DEBUG: Detailed debugging info             │
│   - API request/response details            │
│   - Data transformation steps               │
│   - Variable values                         │
│                                             │
│  INFO: Normal operation                     │
│   - Pipeline steps completed                │
│   - Counts and summaries                    │
│   - Configuration loaded                    │
│                                             │
│  WARNING: Recoverable issues                │
│   - Skipped invalid profiles               │
│   - Retry attempts                          │
│   - Missing optional data                   │
│                                             │
│  ERROR: Failed operations                   │
│   - API errors                              │
│   - Authentication failures                 │
│   - Critical data missing                   │
│                                             │
└────────────────────────────────────────────┘
```

---

## Security Architecture

```
┌─────────────────────────────────────────────────┐
│            Security Layers                       │
├─────────────────────────────────────────────────┤
│                                                  │
│  [1] Credentials Storage                         │
│      - API keys in .env (gitignored)            │
│      - Service account in .json (gitignored)    │
│      - No hardcoded secrets                     │
│                                                  │
│  [2] API Authentication                          │
│      - Google: OAuth2 Service Account           │
│      - Apify: API Token                         │
│      - OpenRouter: API Key                      │
│                                                  │
│  [3] Access Control                              │
│      - Google Sheets: Editor permissions        │
│      - Minimal scope: sheets + drive            │
│      - Service account isolation                │
│                                                  │
│  [4] Data Protection                             │
│      - No local data storage (except logs)      │
│      - All data in Google Sheets (user control) │
│      - Logs rotated/cleaned regularly           │
│                                                  │
│  [5] Rate Limiting                               │
│      - Apify: Built-in throttling               │
│      - OpenRouter: Request spacing              │
│      - Google Sheets: Batch operations          │
│                                                  │
│  [6] Error Masking                               │
│      - API keys masked in logs                  │
│      - Sensitive data not logged                │
│      - Stack traces in debug only               │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## Scalability Architecture

```
Current Scale (Default)
├─ Companies: 30
├─ Profiles per company: 4
├─ Total profiles: 120
├─ Time: 15 minutes
└─ Cost: $3-4

Can Scale To
├─ Companies: 100+
├─ Profiles per company: 10+
├─ Total profiles: 1000+
├─ Time: ~1-2 hours
└─ Cost: ~$30-40

Bottlenecks
├─ Apify scraping speed (rate limited)
├─ OpenRouter API calls (sequential)
├─ Google Sheets API (batch updates)
└─ Network bandwidth

Optimization Opportunities
├─ Parallel OpenRouter scoring (threading)
├─ Batch Apify requests
├─ Caching frequent queries
└─ Local database for deduplication
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│         Development Environment         │
│                                          │
│  - Local machine                         │
│  - Manual runs                           │
│  - Testing & refinement                  │
│  - Command: python main.py              │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│         Production Environment          │
│                                          │
│  Option 1: Local Scheduled              │
│  ├─ Screen/tmux session                │
│  ├─ Windows Task Scheduler             │
│  └─ Command: python main.py --schedule │
│                                          │
│  Option 2: Cloud VM                     │
│  ├─ AWS EC2 / GCP Compute / Azure VM   │
│  ├─ Systemd service                     │
│  ├─ Auto-start on boot                  │
│  └─ Log monitoring                      │
│                                          │
│  Option 3: Docker Container             │
│  ├─ Docker image                        │
│  ├─ Container orchestration             │
│  ├─ Easy deployment                     │
│  └─ Portable                            │
│                                          │
│  Option 4: Serverless (Advanced)        │
│  ├─ AWS Lambda                          │
│  ├─ CloudWatch Events trigger           │
│  ├─ Cost-effective                      │
│  └─ Requires adaptation                 │
└─────────────────────────────────────────┘
```

---

## System State Diagram

```
┌──────────┐
│   IDLE   │
└────┬─────┘
     │
     │ User runs: python main.py
     │
     ▼
┌──────────────┐
│  LOADING     │  (Load config, connect APIs)
└────┬─────────┘
     │
     ▼
┌──────────────┐
│  SCRAPING    │  (Apify: Companies → Employees)
│  ▪ Company 1 │
│  ▪ Company 2 │
│  ▪ ...       │
└────┬─────────┘
     │
     ▼
┌──────────────┐
│  SCORING     │  (OpenRouter: AI scoring)
│  ▪ Profile 1 │
│  ▪ Profile 2 │
│  ▪ ...       │
└────┬─────────┘
     │
     ▼
┌──────────────┐
│  WRITING     │  (Google Sheets: Append results)
└────┬─────────┘
     │
     ▼
┌──────────────┐
│  COMPLETE    │  (Log summary, exit)
└────┬─────────┘
     │
     ├─ Manual run ──→ EXIT
     │
     └─ Scheduled ───→ WAITING
                       └─→ LOADING (after interval)
```

---

## Technology Stack Diagram

```
┌─────────────────────────────────────────────┐
│             Application Layer                │
│                                              │
│  ┌────────────┐    ┌───────────────────┐   │
│  │  main.py   │◄──►│  src/ modules     │   │
│  │  (CLI)     │    │  (Business Logic) │   │
│  └────────────┘    └───────────────────┘   │
└─────────────────────────────────────────────┘
               │              │
               ▼              ▼
┌──────────────────────────────────────────────┐
│             Framework Layer                   │
│                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Pydantic │  │ Schedule │  │ Logging  │   │
│  │ (Models) │  │ (Cron)   │  │ (Logs)   │   │
│  └──────────┘  └──────────┘  └──────────┘   │
└──────────────────────────────────────────────┘
               │              │
               ▼              ▼
┌──────────────────────────────────────────────┐
│              SDK/Client Layer                 │
│                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ gspread  │  │  apify   │  │  openai  │   │
│  │ (Google) │  │ (Scrape) │  │  (AI)    │   │
│  └──────────┘  └──────────┘  └──────────┘   │
└──────────────────────────────────────────────┘
               │              │
               ▼              ▼
┌──────────────────────────────────────────────┐
│              External APIs                    │
│                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Google  │  │  Apify   │  │OpenRouter│   │
│  │  Sheets  │  │   API    │  │   API    │   │
│  └──────────┘  └──────────┘  └──────────┘   │
└──────────────────────────────────────────────┘
               │              │
               ▼              ▼
┌──────────────────────────────────────────────┐
│              Data Sources                     │
│                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Google  │  │ LinkedIn │  │  Claude  │   │
│  │  Drive   │  │  (Data)  │  │  AI      │   │
│  └──────────┘  └──────────┘  └──────────┘   │
└──────────────────────────────────────────────┘
```

---

This architecture is designed to be:
- **Modular:** Each component has a single responsibility
- **Scalable:** Easy to increase limits and add features
- **Maintainable:** Clear separation of concerns
- **Reliable:** Comprehensive error handling
- **Secure:** Proper credential management
- **Configurable:** No hardcoded values
