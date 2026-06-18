"""
Apify Scraper - LinkedIn Company and Employee Scraping
"""
import logging
import time
from typing import List, Dict, Any
from apify_client import ApifyClient
from .models import ICPSettings, CompanyProfile, EmployeeProfile

logger = logging.getLogger(__name__)


class ApifyScraper:
    """Scrape LinkedIn companies and employees using Apify"""

    def __init__(self, api_token: str, company_actor: str, employee_actor: str,
                 timeout: int = 300, max_retries: int = 3):
        """
        Initialize Apify Scraper

        Args:
            api_token: Apify API token
            company_actor: Company search scraper actor ID
            employee_actor: Employee scraper actor ID
            timeout: Timeout in seconds
            max_retries: Max retry attempts
        """
        self.client = ApifyClient(api_token)
        self.company_actor = company_actor
        self.employee_actor = employee_actor
        self.timeout = timeout
        self.max_retries = max_retries

    def find_companies(self, icp: ICPSettings, max_companies: int = 30) -> List[CompanyProfile]:
        """
        Find companies matching ICP criteria

        Args:
            icp: ICP settings
            max_companies: Maximum number of companies to return

        Returns:
            List of CompanyProfile objects
        """
        logger.info(f"Searching for companies matching ICP (max: {max_companies})")

        # Build structured filter (the format client provided)
        run_input = self._build_company_input(icp, max_companies)
        logger.info(f"Using structured filters: industries={len(run_input.get('industryIds', []))}, locations={len(run_input.get('locations', []))}")

        try:
            run = self.client.actor(self.company_actor).call(run_input=run_input)
            # Handle both dict and object responses from Apify
            dataset_id = run.get("defaultDatasetId") if isinstance(run, dict) else run.get('default_dataset_id')
            dataset_items = self.client.dataset(dataset_id).list_items().items

            companies = []
            for item in dataset_items[:max_companies]:
                try:
                    company = CompanyProfile(
                        name=item.get('name', ''),
                        linkedin_url=item.get('linkedinUrl', ''),
                        industry=item.get('industry'),
                        company_size=self._parse_company_size(item.get('companySize')),
                        location=item.get('location'),
                        description=item.get('description'),
                        website=item.get('website')
                    )
                    companies.append(company)
                except Exception as e:
                    logger.warning(f"Failed to parse company: {e}")
                    continue

            logger.info(f"Found {len(companies)} companies")
            return companies

        except Exception as e:
            logger.error(f"Failed to scrape companies: {e}")
            raise

    def find_employees(self, company: CompanyProfile, icp: ICPSettings,
                      max_profiles: int = 4) -> List[EmployeeProfile]:
        """
        Find employees at a company matching ICP criteria

        Args:
            company: Company profile
            icp: ICP settings
            max_profiles: Maximum profiles per company

        Returns:
            List of EmployeeProfile objects
        """
        logger.info(f"Scraping employees from {company.name} (max: {max_profiles})")

        # Build search query: "people at [Company] [Job Titles]"
        job_titles = ' OR '.join(icp.target_job_titles[:3]) if icp.target_job_titles else 'CEO CTO Founder'
        search_query = f"people at {company.name} {job_titles}"

        run_input = {
            "searchQuery": search_query,
            "maxItems": max_profiles,
            "scraperMode": "full"
        }

        logger.info(f"Searching: {search_query}")

        try:
            run = self.client.actor(self.employee_actor).call(run_input=run_input)
            # Handle both dict and object responses from Apify
            dataset_id = run.get("defaultDatasetId") if isinstance(run, dict) else run.get('default_dataset_id')
            dataset_items = self.client.dataset(dataset_id).list_items().items

            employees = []
            for item in dataset_items[:max_profiles]:
                try:
                    # Handle the actual API response format
                    full_name = f"{item.get('firstName', '')} {item.get('lastName', '')}".strip()
                    location_data = item.get('location', {})
                    location_str = location_data.get('linkedinText') if isinstance(location_data, dict) else str(location_data) if location_data else None

                    employee = EmployeeProfile(
                        full_name=full_name or item.get('fullName', 'N/A'),
                        job_title=item.get('headline', ''),
                        linkedin_url=item.get('linkedinUrl', ''),
                        company_name=company.name,
                        company_url=company.linkedin_url,
                        location=location_str,
                        industry=company.industry,
                        company_size=company.company_size,
                        seniority_level=self._extract_seniority(item.get('headline', '')),
                        department=self._extract_department(item.get('headline', '')),
                        profile_summary=item.get('about'),
                        email=None,  # Not available without premium
                        phone=None   # Not available without premium
                    )
                    employees.append(employee)
                except Exception as e:
                    logger.warning(f"Failed to parse employee: {e}")
                    continue

            logger.info(f"Found {len(employees)} employees at {company.name}")
            return employees

        except Exception as e:
            logger.error(f"Failed to scrape employees from {company.name}: {e}")
            return []

    def scrape_all(self, icp: ICPSettings, max_companies: int = 30,
                   max_profiles_per_company: int = 4) -> List[EmployeeProfile]:
        """
        Full scraping pipeline: companies → employees

        Args:
            icp: ICP settings
            max_companies: Maximum companies to scrape
            max_profiles_per_company: Maximum profiles per company

        Returns:
            List of all employee profiles
        """
        all_employees = []

        # Step 1: Find companies
        companies = self.find_companies(icp, max_companies)

        # Step 2: For each company, find employees
        for idx, company in enumerate(companies, 1):
            logger.info(f"Processing company {idx}/{len(companies)}: {company.name}")

            try:
                employees = self.find_employees(company, icp, max_profiles_per_company)
                all_employees.extend(employees)

                # Rate limiting
                if idx < len(companies):
                    time.sleep(2)

            except Exception as e:
                logger.error(f"Error processing {company.name}: {e}")
                continue

        logger.info(f"Scraping complete: {len(all_employees)} total profiles from {len(companies)} companies")
        return all_employees

    def _build_company_input(self, icp: ICPSettings, max_companies: int) -> dict:
        """Build structured input for harvestapi/linkedin-company-search"""
        # Industry mapping (LinkedIn numeric IDs)
        industry_map = {
            'Software': '4',
            'SaaS': '4',
            'Software Development': '4',
            'Technology': '4',
            'IT Services': '96',
            'Information Technology': '96',
            'Computer & Network Security': '118',
            'Cybersecurity': '118',
            'Financial Services': '43',
            'FinTech': '43',
            'Internet': '6',
            'E-commerce': '96',
            'Cloud Computing': '96',
            'AI': '4',
            'Machine Learning': '4',
        }

        # Convert company size to LinkedIn ranges
        size_ranges = []
        if icp.company_size_min and icp.company_size_max:
            # Map to LinkedIn ranges: "1-10", "11-50", "51-200", "201-500", "501-1000", "1001-5000", "5001-10000", "10001+"
            if icp.company_size_max <= 50:
                size_ranges = ["1-10", "11-50"]
            elif icp.company_size_max <= 200:
                size_ranges = ["11-50", "51-200"]
            elif icp.company_size_max <= 500:
                size_ranges = ["51-200", "201-500"]
            elif icp.company_size_max <= 1000:
                size_ranges = ["201-500", "501-1000"]
            else:
                size_ranges = ["501-1000", "1001-5000", "5001-10000"]

        # Convert industry names to IDs
        industry_ids = []
        for industry in icp.industries:
            if industry in industry_map:
                industry_id = industry_map[industry]
                if industry_id not in industry_ids:
                    industry_ids.append(industry_id)

        # Build the input in the format client provided
        run_input = {
            "companySize": size_ranges if size_ranges else ["51-200", "201-500", "501-1000"],
            "industryIds": industry_ids if industry_ids else ["4", "96"],  # Default to Software & IT
            "locations": icp.countries if icp.countries else ["France"],
            "maxItems": max_companies,
            "scraperMode": "full",
            "startPage": 1,
            "takePages": 20
        }

        return run_input

    def _build_company_search_query(self, icp: ICPSettings) -> str:
        """Build LinkedIn search query from ICP settings"""
        query_parts = []

        if icp.industries:
            query_parts.append(f"industry:({' OR '.join(icp.industries)})")

        if icp.countries:
            query_parts.append(f"location:({' OR '.join(icp.countries)})")

        if icp.company_types:
            query_parts.append(f"type:({' OR '.join(icp.company_types)})")

        return ' '.join(query_parts) if query_parts else "*"

    @staticmethod
    def _parse_company_size(size_str: str) -> int:
        """Parse company size string to integer"""
        if not size_str:
            return None

        try:
            # Handle ranges like "51-200"
            if '-' in str(size_str):
                parts = str(size_str).split('-')
                # Return midpoint
                return (int(parts[0]) + int(parts[1])) // 2
            # Handle "10,000+" format
            size_str = str(size_str).replace(',', '').replace('+', '')
            return int(size_str)
        except:
            return None

    @staticmethod
    def _extract_seniority(job_title: str) -> str:
        """Extract seniority level from job title"""
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
