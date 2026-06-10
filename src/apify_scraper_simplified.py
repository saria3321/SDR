"""
Apify Scraper - Simplified Version Using Real Apify Actors
This version uses harvestapi/linkedin-profile-search which actually exists
"""
import logging
import time
from typing import List
from apify_client import ApifyClient
from .models import ICPSettings, CompanyProfile, EmployeeProfile

logger = logging.getLogger(__name__)


class ApifyScraperSimplified:
    """
    Simplified scraper using harvestapi/linkedin-profile-search
    This actor exists and is the most popular on Apify (20K+ users)
    """

    def __init__(self, api_token: str, timeout: int = 300):
        """
        Initialize Apify Scraper

        Args:
            api_token: Apify API token
            timeout: Timeout in seconds
        """
        self.client = ApifyClient(api_token)
        self.actor_id = "harvestapi/linkedin-profile-search"
        self.timeout = timeout

    def search_profiles_directly(self, icp: ICPSettings, max_profiles: int = 120) -> List[EmployeeProfile]:
        """
        Search LinkedIn profiles directly using ICP criteria
        This is simpler than two-stage scraping

        Args:
            icp: ICP settings
            max_profiles: Maximum number of profiles to return

        Returns:
            List of EmployeeProfile objects
        """
        logger.info(f"Searching LinkedIn profiles (max: {max_profiles})")

        # Build search keywords from ICP
        search_keywords = []

        if icp.target_job_titles:
            # Use first few job titles as search keywords
            search_keywords.extend(icp.target_job_titles[:3])

        if icp.industries:
            search_keywords.extend(icp.industries[:2])

        search_string = ' '.join(search_keywords)

        # Build location filter
        locations = icp.countries if icp.countries else []

        run_input = {
            "search": search_string,
            "locations": locations,
            "maxResults": max_profiles,
            "includeFullProfiles": True,
        }

        try:
            logger.info(f"Running Apify actor with search: '{search_string}'")
            logger.info(f"Locations: {locations}")

            run = self.client.actor(self.actor_id).call(run_input=run_input)
            dataset_items = self.client.dataset(run["defaultDatasetId"]).list_items().items

            employees = []
            for item in dataset_items:
                try:
                    # Parse the profile data
                    employee = self._parse_profile(item)
                    if employee:
                        employees.append(employee)
                except Exception as e:
                    logger.warning(f"Failed to parse profile: {e}")
                    continue

            logger.info(f"Found {len(employees)} profiles")
            return employees

        except Exception as e:
            logger.error(f"Failed to scrape profiles: {e}")
            raise

    def _parse_profile(self, item: dict) -> EmployeeProfile:
        """Parse profile data from Apify result"""
        try:
            # Different actors may have different field names
            # Try common variations
            name = (item.get('fullName') or
                   item.get('name') or
                   item.get('full_name') or
                   f"{item.get('firstName', '')} {item.get('lastName', '')}").strip()

            job_title = (item.get('title') or
                        item.get('headline') or
                        item.get('jobTitle') or
                        '')

            linkedin_url = (item.get('profileUrl') or
                          item.get('url') or
                          item.get('linkedinUrl') or
                          '')

            location = (item.get('location') or
                       item.get('geo') or
                       '')

            # Company information
            company_name = ''
            company_size = None
            industry = ''

            # Try to get current company
            if 'company' in item:
                company_name = item['company']
            elif 'experience' in item and item['experience']:
                # Get first (current) job
                current_job = item['experience'][0]
                company_name = current_job.get('companyName', '')

            # Try to get industry
            if 'industry' in item:
                industry = item['industry']

            summary = (item.get('summary') or
                      item.get('description') or
                      item.get('about') or
                      '')

            employee = EmployeeProfile(
                full_name=name,
                job_title=job_title,
                linkedin_url=linkedin_url,
                company_name=company_name,
                location=location,
                industry=industry,
                company_size=company_size,
                seniority_level=self._extract_seniority(job_title),
                department=self._extract_department(job_title),
                profile_summary=summary,
                email=item.get('email'),
                phone=item.get('phone')
            )

            return employee

        except Exception as e:
            logger.error(f"Error parsing profile: {e}")
            return None

    @staticmethod
    def _extract_seniority(job_title: str) -> str:
        """Extract seniority level from job title"""
        if not job_title:
            return 'Other'

        title_lower = job_title.lower()

        seniority_map = {
            'founder': 'Founder',
            'ceo': 'C-Level',
            'cto': 'C-Level',
            'cfo': 'C-Level',
            'coo': 'C-Level',
            'cmo': 'C-Level',
            'chief': 'C-Level',
            'vp': 'VP',
            'vice president': 'VP',
            'director': 'Director',
            'head': 'Head',
            'manager': 'Manager',
            'lead': 'Lead',
            'senior': 'Senior',
            'junior': 'Junior'
        }

        for keyword, level in seniority_map.items():
            if keyword in title_lower:
                return level

        return 'Other'

    @staticmethod
    def _extract_department(job_title: str) -> str:
        """Extract department from job title"""
        if not job_title:
            return 'Other'

        title_lower = job_title.lower()

        department_map = {
            'sales': 'Sales',
            'marketing': 'Marketing',
            'operations': 'Operations',
            'engineer': 'Engineering',
            'technology': 'Engineering',
            'product': 'Product',
            'hr': 'HR',
            'human resources': 'HR',
            'finance': 'Finance',
            'legal': 'Legal',
            'customer': 'Customer Success'
        }

        for keyword, dept in department_map.items():
            if keyword in title_lower:
                return dept

        return 'Other'
