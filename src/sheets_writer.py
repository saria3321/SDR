"""
Google Sheets Writer - Write qualified leads to Google Sheets
"""
import logging
from typing import List, Set
import gspread
from google.oauth2.service_account import Credentials
from .models import ScoredLead

logger = logging.getLogger(__name__)


class SheetsWriter:
    """Write qualified leads to Google Sheets with duplicate detection"""

    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    HEADERS = [
        'Date Added',
        'New Lead',
        'Lead Score',
        'Full Name',
        'Job Title',
        'Company Name',
        'Company Size',
        'Industry',
        'Location',
        'LinkedIn URL',
        'Email',
        'Phone',
        'Seniority Level',
        'Department',
        'Years of Experience',
        'AI Reasoning',
        'Profile Summary',
        'Company URL',
        'Last Updated'
    ]

    def __init__(self, credentials_path: str, sheet_id: str, tab_name: str = "Qualified Leads"):
        """
        Initialize Sheets Writer

        Args:
            credentials_path: Path to Google Service Account JSON
            sheet_id: Google Sheets ID
            tab_name: Tab name for output
        """
        self.credentials_path = credentials_path
        self.sheet_id = sheet_id
        self.tab_name = tab_name
        self.client = None
        self.worksheet = None

    def connect(self):
        """Establish connection to Google Sheets"""
        try:
            creds = Credentials.from_service_account_file(
                self.credentials_path,
                scopes=self.SCOPES
            )
            self.client = gspread.authorize(creds)
            logger.info("Successfully connected to Google Sheets")
        except Exception as e:
            logger.error(f"Failed to connect to Google Sheets: {e}")
            raise

    def initialize_sheet(self):
        """Initialize or get the output sheet with headers"""
        if not self.client:
            self.connect()

        try:
            sheet = self.client.open_by_key(self.sheet_id)

            # Try to get existing worksheet
            try:
                self.worksheet = sheet.worksheet(self.tab_name)
                logger.info(f"Found existing sheet: {self.tab_name}")

                # Check if headers exist
                existing_headers = self.worksheet.row_values(1)
                if not existing_headers or existing_headers != self.HEADERS:
                    logger.info("Updating headers")
                    self.worksheet.update('A1:S1', [self.HEADERS])

            except gspread.WorksheetNotFound:
                # Create new worksheet
                logger.info(f"Creating new sheet: {self.tab_name}")
                self.worksheet = sheet.add_worksheet(
                    title=self.tab_name,
                    rows=1000,
                    cols=len(self.HEADERS)
                )
                self.worksheet.update('A1:S1', [self.HEADERS])

        except Exception as e:
            logger.error(f"Failed to initialize sheet: {e}")
            raise

    def get_existing_linkedin_urls(self, max_rows: int = 1000) -> Set[str]:
        """
        Get set of existing LinkedIn URLs to prevent duplicates

        Args:
            max_rows: Maximum rows to check

        Returns:
            Set of LinkedIn URLs already in sheet
        """
        if not self.worksheet:
            self.initialize_sheet()

        try:
            # Get LinkedIn URL column (column J, index 9)
            url_column = self.worksheet.col_values(10)  # 1-indexed

            # Skip header
            existing_urls = set(url_column[1:max_rows]) if len(url_column) > 1 else set()
            logger.info(f"Found {len(existing_urls)} existing leads in sheet")
            return existing_urls

        except Exception as e:
            logger.error(f"Failed to get existing URLs: {e}")
            return set()

    def write_leads(self, scored_leads: List[ScoredLead], duplicate_check: bool = True) -> int:
        """
        Write qualified leads to Google Sheets

        Args:
            scored_leads: List of scored leads
            duplicate_check: Whether to check for duplicates

        Returns:
            Number of new leads added
        """
        if not self.worksheet:
            self.initialize_sheet()

        if not scored_leads:
            logger.info("No leads to write")
            return 0

        # Check for existing leads
        existing_urls = set()
        if duplicate_check:
            existing_urls = self.get_existing_linkedin_urls()

        # Prepare rows
        new_rows = []
        for lead in scored_leads:
            # Skip if duplicate
            if lead.profile.linkedin_url in existing_urls:
                logger.info(f"Skipping duplicate: {lead.profile.full_name}")
                continue

            row = [
                lead.date_added,
                'YES' if lead.is_new else 'NO',
                lead.score,
                lead.profile.full_name,
                lead.profile.job_title,
                lead.profile.company_name,
                lead.profile.company_size or '',
                lead.profile.industry or '',
                lead.profile.location or '',
                lead.profile.linkedin_url,
                lead.profile.email or '',
                lead.profile.phone or '',
                lead.profile.seniority_level or '',
                lead.profile.department or '',
                lead.profile.years_of_experience or '',
                lead.reasoning,
                lead.profile.profile_summary or '',
                lead.profile.company_url or '',
                lead.date_added
            ]
            new_rows.append(row)

        if not new_rows:
            logger.info("No new leads to add (all duplicates)")
            return 0

        try:
            # Append all new rows
            self.worksheet.append_rows(new_rows)
            logger.info(f"Successfully added {len(new_rows)} new leads to sheet")

            # Mark old leads as not new
            self._update_new_lead_flags()

            return len(new_rows)

        except Exception as e:
            logger.error(f"Failed to write leads to sheet: {e}")
            raise

    def _update_new_lead_flags(self):
        """Update 'New Lead' column to mark previous leads as NO"""
        try:
            # Get all values in New Lead column (column B)
            new_lead_col = self.worksheet.col_values(2)

            # Find all YES values except the most recent batch
            # We'll keep the last added batch as YES
            updates = []
            for i, value in enumerate(new_lead_col[1:], start=2):  # Skip header
                if value == 'YES':
                    # Only update if not in the last 100 rows (recent batch)
                    if i < len(new_lead_col) - 100:
                        updates.append({'range': f'B{i}', 'values': [['NO']]})

            if updates and len(updates) > 0:
                # Batch update
                self.worksheet.batch_update(updates[:100])  # Limit batch size
                logger.info(f"Updated {len(updates[:100])} old leads to 'NO'")

        except Exception as e:
            logger.warning(f"Failed to update new lead flags: {e}")

    def clear_new_flags(self):
        """Clear all 'New Lead' flags (set to NO)"""
        if not self.worksheet:
            self.initialize_sheet()

        try:
            # Get all rows
            all_values = self.worksheet.get_all_values()

            updates = []
            for i, row in enumerate(all_values[1:], start=2):  # Skip header
                if len(row) > 1 and row[1] == 'YES':
                    updates.append({'range': f'B{i}', 'values': [['NO']]})

            if updates:
                # Batch update in chunks of 100
                for i in range(0, len(updates), 100):
                    batch = updates[i:i+100]
                    self.worksheet.batch_update(batch)

                logger.info(f"Cleared {len(updates)} new lead flags")

        except Exception as e:
            logger.error(f"Failed to clear new flags: {e}")
