"""
AI SDR - Main Entry Point
Automated Lead Generation & Qualification System
"""
import os
import sys
import logging
import argparse
from pathlib import Path
from dotenv import load_dotenv
import yaml

from src.icp_loader import ICPLoader
from src.apify_scraper import ApifyScraper
from src.ai_scorer import AIScorer
from src.sheets_writer import SheetsWriter
from src.scheduler import JobScheduler


def setup_logging(config: dict):
    """Setup logging configuration"""
    log_level = config.get('logging', {}).get('level', 'INFO')
    log_file = config.get('logging', {}).get('file', 'logs/sdr.log')

    # Create logs directory if it doesn't exist
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )


def load_config(config_path: str = 'config.yaml') -> dict:
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)


def validate_env_vars():
    """Validate required environment variables"""
    required_vars = [
        'APIFY_API_TOKEN',
        'OPENROUTER_API_KEY',
        'GOOGLE_SHEETS_CREDENTIALS_PATH',
        'ICP_SHEET_ID',
        'OUTPUT_SHEET_ID'
    ]

    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        print(f"Error: Missing required environment variables: {', '.join(missing)}")
        print("Please create a .env file with all required variables.")
        sys.exit(1)


def run_pipeline(config: dict, max_companies: int = None, max_profiles: int = None):
    """
    Run the complete SDR pipeline

    Args:
        config: Configuration dictionary
        max_companies: Override max companies from config
        max_profiles: Override max profiles per company from config
    """
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("Starting AI SDR Pipeline")
    logger.info("=" * 60)

    # Get limits
    limits = config.get('limits', {})
    max_companies = max_companies or limits.get('max_companies', 30)
    max_profiles_per_company = max_profiles or limits.get('max_profiles_per_company', 4)

    logger.info(f"Limits: {max_companies} companies, {max_profiles_per_company} profiles/company")

    try:
        # Step 1: Load ICP Settings
        logger.info("\n[Step 1/5] Loading ICP Settings from Google Sheets")
        icp_loader = ICPLoader(
            credentials_path=os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH'),
            sheet_id=os.getenv('ICP_SHEET_ID'),
            tab_name=os.getenv('ICP_SHEET_TAB_NAME', 'ICP Settings')
        )
        icp = icp_loader.load_icp()

        logger.info(f"✓ ICP Loaded: {len(icp.industries)} industries, "
                   f"{len(icp.target_job_titles)} target titles, "
                   f"{len(icp.countries)} countries")

        # Step 2: Scrape Companies and Employees
        logger.info("\n[Step 2/5] Scraping LinkedIn Data via Apify")
        scraper = ApifyScraper(
            api_token=os.getenv('APIFY_API_TOKEN'),
            company_actor=os.getenv('APIFY_COMPANY_SCRAPER_ACTOR'),
            employee_actor=os.getenv('APIFY_EMPLOYEE_SCRAPER_ACTOR'),
            timeout=config.get('apify', {}).get('timeout', 300),
            max_retries=config.get('apify', {}).get('max_retries', 3)
        )

        all_profiles = scraper.scrape_all(
            icp=icp,
            max_companies=max_companies,
            max_profiles_per_company=max_profiles_per_company
        )

        logger.info(f"✓ Scraped {len(all_profiles)} total employee profiles")

        if not all_profiles:
            logger.warning("No profiles found. Exiting.")
            return

        # Step 3: Score Leads with AI
        logger.info("\n[Step 3/5] Scoring Leads with AI (OpenRouter)")
        scorer = AIScorer(
            api_key=os.getenv('OPENROUTER_API_KEY'),
            model=config.get('openrouter', {}).get('model', 'anthropic/claude-3.5-sonnet'),
            temperature=config.get('openrouter', {}).get('temperature', 0.3),
            max_tokens=config.get('openrouter', {}).get('max_tokens', 500)
        )

        min_score = config.get('scoring', {}).get('min_qualified_score', 60)
        qualified_leads = scorer.score_batch(all_profiles, icp, min_score=min_score)

        logger.info(f"✓ Qualified {len(qualified_leads)} leads (score >= {min_score})")

        if not qualified_leads:
            logger.warning("No qualified leads found. Exiting.")
            return

        # Step 4: Write to Google Sheets
        logger.info("\n[Step 4/5] Writing to Google Sheets")
        writer = SheetsWriter(
            credentials_path=os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH'),
            sheet_id=os.getenv('OUTPUT_SHEET_ID'),
            tab_name=os.getenv('OUTPUT_SHEET_TAB_NAME', 'Qualified Leads')
        )

        new_leads_count = writer.write_leads(qualified_leads, duplicate_check=True)

        logger.info(f"✓ Added {new_leads_count} new leads to sheet")

        # Step 5: Summary
        logger.info("\n[Step 5/5] Pipeline Summary")
        logger.info("=" * 60)
        logger.info(f"Companies Scraped: {max_companies}")
        logger.info(f"Profiles Scraped: {len(all_profiles)}")
        logger.info(f"Qualified Leads: {len(qualified_leads)}")
        logger.info(f"New Leads Added: {new_leads_count}")
        logger.info(f"Duplicates Skipped: {len(qualified_leads) - new_leads_count}")
        logger.info("=" * 60)
        logger.info("✓ Pipeline completed successfully!")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        raise


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='AI SDR - Automated Lead Generation')
    parser.add_argument('--schedule', action='store_true',
                       help='Run on schedule (continuous mode)')
    parser.add_argument('--max-companies', type=int,
                       help='Override max companies limit')
    parser.add_argument('--max-profiles', type=int,
                       help='Override max profiles per company')
    parser.add_argument('--config', type=str, default='config.yaml',
                       help='Path to config file')

    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    # Validate environment
    validate_env_vars()

    # Load configuration
    config = load_config(args.config)

    # Setup logging
    setup_logging(config)

    logger = logging.getLogger(__name__)

    # Run pipeline
    if args.schedule:
        # Scheduled mode
        interval = config.get('scheduling', {}).get('interval_hours', 24)

        def job():
            run_pipeline(config, args.max_companies, args.max_profiles)

        scheduler = JobScheduler(job, interval_hours=interval)
        logger.info(f"Running in scheduled mode (every {interval} hours)")
        scheduler.run_scheduled()
    else:
        # One-time run
        logger.info("Running in one-time mode")
        run_pipeline(config, args.max_companies, args.max_profiles)


if __name__ == "__main__":
    main()
