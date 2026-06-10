"""
Helper script to create ICP template in Google Sheets
Run this after you've set up your Google credentials
"""
import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

# Load environment
load_dotenv()

# Google Sheets configuration
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

HEADERS = [
    'Industries',
    'Company Size Min',
    'Company Size Max',
    'Countries',
    'Target Job Titles',
    'Required Keywords',
    'Seniority Levels',
    'Departments',
    'Company Types',
    'Languages',
    'Excluded Keywords',
    'Years Experience Min',
    'Years Experience Max'
]

EXAMPLE_ROW = [
    'Software, SaaS, Technology, IT Services',
    '10',
    '500',
    'France, Belgium, Switzerland',
    'CEO, CTO, Founder, VP Sales, Head of Sales, Director of Sales',
    'B2B, Enterprise, SaaS, Cloud',
    'C-Level, VP, Director, Founder',
    'Sales, Marketing, Operations, Business Development',
    'Startup, SMB',
    'French, English',
    'Agency, Freelance, Consulting',
    '3',
    '20'
]

def create_icp_template():
    """Create ICP template in Google Sheets"""
    print("Creating ICP Template in Google Sheets...")

    # Get credentials
    credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
    sheet_id = os.getenv('ICP_SHEET_ID')
    tab_name = os.getenv('ICP_SHEET_TAB_NAME', 'ICP Settings')

    if not credentials_path or not sheet_id:
        print("ERROR: Please set GOOGLE_SHEETS_CREDENTIALS_PATH and ICP_SHEET_ID in .env")
        return

    try:
        # Connect to Google Sheets
        creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
        client = gspread.authorize(creds)

        # Open sheet
        sheet = client.open_by_key(sheet_id)

        # Try to get or create worksheet
        try:
            worksheet = sheet.worksheet(tab_name)
            print(f"Found existing worksheet: {tab_name}")
        except gspread.WorksheetNotFound:
            print(f"Creating new worksheet: {tab_name}")
            worksheet = sheet.add_worksheet(title=tab_name, rows=100, cols=len(HEADERS))

        # Write headers
        print("Writing headers...")
        worksheet.update('A1:M1', [HEADERS])

        # Format headers (bold)
        worksheet.format('A1:M1', {
            "textFormat": {"bold": True},
            "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9}
        })

        # Write example row
        print("Writing example ICP configuration...")
        worksheet.update('A2:M2', [EXAMPLE_ROW])

        # Add instructions
        instructions = [
            ["INSTRUCTIONS:"],
            ["1. Edit the values in Row 2 to match your Ideal Customer Profile"],
            ["2. Use comma-separated values for multiple items (e.g., 'France, Belgium, Switzerland')"],
            ["3. Leave fields empty if you don't want to filter by that criterion"],
            ["4. Only the first data row (Row 2) is used - additional rows are ignored"],
            ["5. After editing, save and run the main.py script"],
            [""],
            ["FIELD DESCRIPTIONS:"],
            ["- Industries: Target industries (e.g., 'Software, SaaS, Technology')"],
            ["- Company Size Min/Max: Employee count range (e.g., 10 to 500)"],
            ["- Countries: Target countries/regions (e.g., 'France, Belgium')"],
            ["- Target Job Titles: Desired job titles (e.g., 'CEO, CTO, Founder')"],
            ["- Required Keywords: Keywords that should appear in profiles"],
            ["- Seniority Levels: Target seniority (e.g., 'C-Level, VP, Director')"],
            ["- Departments: Target departments (e.g., 'Sales, Marketing')"],
            ["- Company Types: Types of companies (e.g., 'Startup, SMB, Enterprise')"],
            ["- Languages: Required languages (e.g., 'French, English')"],
            ["- Excluded Keywords: Keywords to filter out (e.g., 'Agency, Freelance')"],
            ["- Years Experience Min/Max: Experience range in years"]
        ]

        worksheet.update('O1:O19', instructions)

        print("✓ ICP template created successfully!")
        print(f"✓ Sheet URL: https://docs.google.com/spreadsheets/d/{sheet_id}")
        print("\nNext steps:")
        print("1. Edit the values in Row 2 to match your ICP")
        print("2. Run: python main.py")

    except Exception as e:
        print(f"ERROR: {e}")
        print("\nTroubleshooting:")
        print("1. Check that credentials.json exists")
        print("2. Verify the Sheet ID in .env is correct")
        print("3. Make sure the service account has access to the sheet")

if __name__ == "__main__":
    create_icp_template()
