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

        # Build search query from ICP
        search_query = self._build_company_search_query(icp)

        run_input = {
            "searchQuery": search_query,
            "maxResults": max_companies,
            "includeCompanyDetails": True
        }

        try:
            run = self.client.actor(self.company_actor).call(run_input=run_input)
            dataset_items = self.client.dataset(run["defaultDatasetId"]).list_items().items

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

        # Build job title filters
        job_title_filters = icp.target_job_titles if icp.target_job_titles else []

        run_input = {
            "companyUrl": company.linkedin_url,
            "jobTitles": job_title_filters,
            "maxResults": max_profiles,
            "includeProfileDetails": True
        }

        try:
            run = self.client.actor(self.employee_actor).call(run_input=run_input)
            dataset_items = self.client.dataset(run["defaultDatasetId"]).list_items().items

            employees = []
            for item in dataset_items[:max_profiles]:
                try:
                    employee = EmployeeProfile(
                        full_name=item.get('name', ''),
                        job_title=item.get('jobTitle', ''),
                        linkedin_url=item.get('linkedinUrl', ''),
                        company_name=company.name,
                        company_url=company.linkedin_url,
                        location=item.get('location'),
                        industry=company.industry,
                        company_size=company.company_size,
                        seniority_level=self._extract_seniority(item.get('jobTitle', '')),
                        department=self._extract_department(item.get('jobTitle', '')),
                        profile_summary=item.get('summary'),
                        email=item.get('email'),
                        phone=item.get('phone')
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
