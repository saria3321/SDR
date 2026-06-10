"""
Utility Script - Clear all "New Lead" flags in Google Sheets
Run this when you've reviewed all new leads and want to reset the flags
"""
import os
from dotenv import load_dotenv
from src.sheets_writer import SheetsWriter
import logging

logging.basicConfig(level=logging.INFO)

def main():
    """Clear all new lead flags"""
    load_dotenv()

    print("Clearing all 'New Lead' flags...")

    writer = SheetsWriter(
        credentials_path=os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH'),
        sheet_id=os.getenv('OUTPUT_SHEET_ID'),
        tab_name=os.getenv('OUTPUT_SHEET_TAB_NAME', 'Qualified Leads')
    )

    confirm = input("This will set all 'New Lead' values to 'NO'. Continue? (y/n): ")

    if confirm.lower() == 'y':
        writer.clear_new_flags()
        print("✓ All 'New Lead' flags cleared!")
    else:
        print("Cancelled.")

if __name__ == "__main__":
    main()
