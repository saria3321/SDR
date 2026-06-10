"""
ICP Settings Loader - Reads Ideal Customer Profile from Google Sheets
"""
import os
import logging
from typing import Optional
import gspread
from google.oauth2.service_account import Credentials
from .models import ICPSettings

logger = logging.getLogger(__name__)


class ICPLoader:
    """Load ICP settings from Google Sheets"""

    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    def __init__(self, credentials_path: str, sheet_id: str, tab_name: str = "ICP Settings"):
        """
        Initialize ICP Loader

        Args:
            credentials_path: Path to Google Service Account JSON
            sheet_id: Google Sheets ID
            tab_name: Tab name containing ICP settings
        """
        self.credentials_path = credentials_path
        self.sheet_id = sheet_id
        self.tab_name = tab_name
        self.client = None

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

    def load_icp(self) -> ICPSettings:
        """
        Load ICP settings from Google Sheets

        Returns:
            ICPSettings object with all configuration
        """
        if not self.client:
            self.connect()

        try:
            sheet = self.client.open_by_key(self.sheet_id)
            worksheet = sheet.worksheet(self.tab_name)

            # Get all records as list of dictionaries
            records = worksheet.get_all_records()

            if not records:
                logger.warning("No ICP settings found in sheet")
                return ICPSettings()

            # Take first row as the active ICP
            row = records[0]

            icp = ICPSettings(
                industries=self._parse_list(row.get('Industries', '')),
                company_size_min=self._parse_int(row.get('Company Size Min')),
                company_size_max=self._parse_int(row.get('Company Size Max')),
                countries=self._parse_list(row.get('Countries', '')),
                target_job_titles=self._parse_list(row.get('Target Job Titles', '')),
                required_keywords=self._parse_list(row.get('Required Keywords', '')),
                seniority_levels=self._parse_list(row.get('Seniority Levels', '')),
                departments=self._parse_list(row.get('Departments', '')),
                company_types=self._parse_list(row.get('Company Types', '')),
                languages=self._parse_list(row.get('Languages', '')),
                excluded_keywords=self._parse_list(row.get('Excluded Keywords', '')),
                years_experience_min=self._parse_int(row.get('Years Experience Min')),
                years_experience_max=self._parse_int(row.get('Years Experience Max'))
            )

            logger.info(f"Loaded ICP settings: {len(icp.industries)} industries, "
                       f"{len(icp.target_job_titles)} job titles")
            return icp

        except Exception as e:
            logger.error(f"Failed to load ICP settings: {e}")
            raise

    @staticmethod
    def _parse_list(value: str) -> list:
        """Parse comma-separated string into list"""
        if not value or not isinstance(value, str):
            return []
        return [item.strip() for item in value.split(',') if item.strip()]

    @staticmethod
    def _parse_int(value) -> Optional[int]:
        """Parse integer value"""
        if not value:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
