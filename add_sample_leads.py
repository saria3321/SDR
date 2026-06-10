"""
Add Sample Qualified Leads to Google Sheet
For client demo - shows the format and AI scoring
"""
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Sample qualified leads matching your ICP
SAMPLE_LEADS = [
    {
        "Date Added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "New Lead": "YES",
        "Lead Score": 92,
        "Full Name": "Pierre Dubois",
        "Job Title": "CEO & Founder",
        "Company Name": "TechFlow SaaS",
        "Company Size": "150",
        "Industry": "Software, SaaS",
        "Location": "Paris, France",
        "LinkedIn URL": "https://www.linkedin.com/in/pierre-dubois-sample",
        "Email (if available)": "pierre@techflow.fr",
        "Phone": "",
        "Seniority Level": "C-Level",
        "Department": "Executive",
        "Years of Experience": "12",
        "AI Reasoning": "Excellent match: CEO of B2B SaaS company in France, 150 employees, strong enterprise focus. Perfect fit for ICP criteria.",
        "Profile Summary": "CEO and Founder of TechFlow, a B2B SaaS platform for enterprise automation. 12+ years in software industry.",
        "Company URL": "https://www.linkedin.com/company/techflow-sample",
        "Last Updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "Date Added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "New Lead": "YES",
        "Lead Score": 88,
        "Full Name": "Marie Laurent",
        "Job Title": "CTO",
        "Company Name": "CloudSync Technologies",
        "Company Size": "85",
        "Industry": "Software, Technology",
        "Location": "Lyon, France",
        "LinkedIn URL": "https://www.linkedin.com/in/marie-laurent-sample",
        "Email (if available)": "marie.laurent@cloudsync.fr",
        "Phone": "",
        "Seniority Level": "C-Level",
        "Department": "Engineering",
        "Years of Experience": "10",
        "AI Reasoning": "Strong match: CTO of growing tech company, right size (85 employees), enterprise B2B focus, located in France. Good ICP alignment.",
        "Profile Summary": "CTO at CloudSync Technologies, leading engineering team of 30+. Expert in B2B cloud solutions.",
        "Company URL": "https://www.linkedin.com/company/cloudsync-sample",
        "Last Updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "Date Added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "New Lead": "YES",
        "Lead Score": 85,
        "Full Name": "Thomas Schneider",
        "Job Title": "VP of Sales",
        "Company Name": "SwissTech Solutions",
        "Company Size": "220",
        "Industry": "SaaS, Fintech",
        "Location": "Zurich, Switzerland",
        "LinkedIn URL": "https://www.linkedin.com/in/thomas-schneider-sample",
        "Email (if available)": "",
        "Phone": "",
        "Seniority Level": "VP",
        "Department": "Sales",
        "Years of Experience": "8",
        "AI Reasoning": "Good match: VP Sales at SaaS/Fintech company in Switzerland, 220 employees, B2B enterprise market. Matches ICP seniority and industry criteria.",
        "Profile Summary": "VP of Sales at SwissTech, managing enterprise B2B sales across EMEA. 8 years experience in SaaS sales.",
        "Company URL": "https://www.linkedin.com/company/swisstech-sample",
        "Last Updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "Date Added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "New Lead": "YES",
        "Lead Score": 90,
        "Full Name": "Sophie Martin",
        "Job Title": "Founder & CEO",
        "Company Name": "DataFlow AI",
        "Company Size": "95",
        "Industry": "Software, SaaS",
        "Location": "Brussels, Belgium",
        "LinkedIn URL": "https://www.linkedin.com/in/sophie-martin-sample",
        "Email (if available)": "sophie@dataflow.be",
        "Phone": "+32 2 123 4567",
        "Seniority Level": "C-Level",
        "Department": "Executive",
        "Years of Experience": "15",
        "AI Reasoning": "Excellent match: Founder/CEO of B2B SaaS company in Belgium, 95 employees, enterprise AI solutions. Perfect ICP alignment with all criteria.",
        "Profile Summary": "Founder & CEO of DataFlow AI, building enterprise AI automation tools. 15+ years in software and SaaS.",
        "Company URL": "https://www.linkedin.com/company/dataflow-ai-sample",
        "Last Updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "Date Added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "New Lead": "YES",
        "Lead Score": 83,
        "Full Name": "Jean Dupont",
        "Job Title": "VP of Product",
        "Company Name": "FinanceHub SaaS",
        "Company Size": "180",
        "Industry": "Fintech, SaaS",
        "Location": "Paris, France",
        "LinkedIn URL": "https://www.linkedin.com/in/jean-dupont-sample",
        "Email (if available)": "",
        "Phone": "",
        "Seniority Level": "VP",
        "Department": "Product",
        "Years of Experience": "9",
        "AI Reasoning": "Good match: VP Product at Fintech SaaS company, 180 employees, B2B enterprise focus. Meets ICP industry and seniority requirements.",
        "Profile Summary": "VP of Product at FinanceHub, leading product strategy for enterprise fintech solutions. 9 years in SaaS.",
        "Company URL": "https://www.linkedin.com/company/financehub-sample",
        "Last Updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "Date Added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "New Lead": "YES",
        "Lead Score": 87,
        "Full Name": "Lucas Weber",
        "Job Title": "CTO & Co-Founder",
        "Company Name": "CloudCore Systems",
        "Company Size": "120",
        "Industry": "Software, Technology",
        "Location": "Geneva, Switzerland",
        "LinkedIn URL": "https://www.linkedin.com/in/lucas-weber-sample",
        "Email (if available)": "lucas@cloudcore.ch",
        "Phone": "",
        "Seniority Level": "C-Level",
        "Department": "Engineering",
        "Years of Experience": "11",
        "AI Reasoning": "Strong match: CTO/Co-Founder of B2B software company in Switzerland, 120 employees, enterprise cloud solutions. Excellent ICP fit.",
        "Profile Summary": "CTO & Co-Founder at CloudCore Systems, building enterprise cloud infrastructure. 11 years in technology.",
        "Company URL": "https://www.linkedin.com/company/cloudcore-sample",
        "Last Updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
]

def add_sample_leads():
    """Add sample leads to Google Sheet"""
    print("=" * 60)
    print("Adding Sample Qualified Leads to Google Sheet")
    print("=" * 60)

    # Setup credentials
    creds = Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )

    client = gspread.authorize(creds)

    # Open the output sheet
    sheet_id = os.getenv('OUTPUT_SHEET_ID')
    tab_name = 'Sheet1'  # The actual tab name in your sheet

    print(f"Opening sheet: {sheet_id}")
    print(f"Tab: {tab_name}")

    try:
        spreadsheet = client.open_by_key(sheet_id)
        worksheet = spreadsheet.worksheet(tab_name)

        print("Sheet opened successfully!")

        # Get headers (row 1)
        headers = worksheet.row_values(1)
        print(f"Found {len(headers)} columns")

        # Prepare rows
        rows_to_add = []
        for lead in SAMPLE_LEADS:
            row = []
            for header in headers:
                row.append(lead.get(header, ""))
            rows_to_add.append(row)

        # Add all leads at once
        print(f"\nAdding {len(rows_to_add)} sample leads...")
        worksheet.append_rows(rows_to_add, value_input_option='USER_ENTERED')

        print("\n" + "=" * 60)
        print("SUCCESS! Sample leads added to your sheet!")
        print("=" * 60)
        print(f"\nCheck your sheet:")
        print(f"https://docs.google.com/spreadsheets/d/{sheet_id}")
        print(f"\nAdded {len(rows_to_add)} qualified leads with:")
        print("  - Lead scores: 83-92")
        print("  - AI reasoning for each")
        print("  - Complete profile information")
        print("  - LinkedIn URLs for outreach")
        print("\nThese are sample/demo leads to show the client.")
        print("Once Apify is working, you'll get real LinkedIn data!")

    except Exception as e:
        print(f"ERROR: {e}")
        print("\nPossible issues:")
        print("1. Sheet ID might be wrong")
        print("2. Tab name might be different")
        print("3. Service account needs Editor permission on the sheet")
        print("\nService account email:")
        print("hyvop-ai-automation@hyvop-481511.iam.gserviceaccount.com")
        print("\nMake sure this email has Editor access to your sheet!")

if __name__ == "__main__":
    add_sample_leads()
