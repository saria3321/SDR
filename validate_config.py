"""
Configuration Validator - Check and display current configuration
"""
import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

def load_env_config():
    """Load and display environment configuration"""
    load_dotenv()

    config = {
        'Apify API Token': os.getenv('APIFY_API_TOKEN', 'NOT SET'),
        'OpenRouter API Key': os.getenv('OPENROUTER_API_KEY', 'NOT SET'),
        'Google Credentials Path': os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH', 'NOT SET'),
        'ICP Sheet ID': os.getenv('ICP_SHEET_ID', 'NOT SET'),
        'Output Sheet ID': os.getenv('OUTPUT_SHEET_ID', 'NOT SET'),
        'ICP Sheet Tab': os.getenv('ICP_SHEET_TAB_NAME', 'ICP Settings'),
        'Output Sheet Tab': os.getenv('OUTPUT_SHEET_TAB_NAME', 'Qualified Leads'),
        'Company Scraper Actor': os.getenv('APIFY_COMPANY_SCRAPER_ACTOR', 'NOT SET'),
        'Employee Scraper Actor': os.getenv('APIFY_EMPLOYEE_SCRAPER_ACTOR', 'NOT SET'),
    }

    return config

def load_yaml_config():
    """Load and display YAML configuration"""
    try:
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        return {'error': str(e)}

def mask_sensitive(value, show_chars=10):
    """Mask sensitive values"""
    if 'NOT SET' in value:
        return value
    if len(value) > show_chars:
        return value[:show_chars] + '...'
    return '***'

def main():
    """Display and validate configuration"""
    print("=" * 60)
    print("AI SDR - Configuration Validator")
    print("=" * 60)
    print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Environment Variables
    print("[1] Environment Variables (.env)")
    print("-" * 60)

    env_config = load_env_config()
    for key, value in env_config.items():
        # Mask sensitive values
        if 'Token' in key or 'Key' in key:
            display_value = mask_sensitive(value)
        else:
            display_value = value

        status = "✓" if value != 'NOT SET' else "✗"
        print(f"{status} {key:30} {display_value}")

    # Check credentials file
    creds_path = env_config['Google Credentials Path']
    if creds_path != 'NOT SET':
        creds_exists = Path(creds_path).exists()
        status = "✓" if creds_exists else "✗"
        print(f"\n{status} Credentials file exists: {creds_exists}")

    # YAML Configuration
    print("\n[2] YAML Configuration (config.yaml)")
    print("-" * 60)

    yaml_config = load_yaml_config()

    if 'error' in yaml_config:
        print(f"✗ Error loading config.yaml: {yaml_config['error']}")
    else:
        # Limits
        limits = yaml_config.get('limits', {})
        print(f"Max Companies:             {limits.get('max_companies', 'NOT SET')}")
        print(f"Max Profiles per Company:  {limits.get('max_profiles_per_company', 'NOT SET')}")

        # Scheduling
        scheduling = yaml_config.get('scheduling', {})
        print(f"\nScheduling Enabled:        {scheduling.get('enabled', 'NOT SET')}")
        print(f"Interval (hours):          {scheduling.get('interval_hours', 'NOT SET')}")

        # Apify
        apify = yaml_config.get('apify', {})
        print(f"\nApify Timeout (seconds):   {apify.get('timeout', 'NOT SET')}")
        print(f"Apify Max Retries:         {apify.get('max_retries', 'NOT SET')}")

        # OpenRouter
        openrouter = yaml_config.get('openrouter', {})
        print(f"\nOpenRouter Model:          {openrouter.get('model', 'NOT SET')}")
        print(f"Temperature:               {openrouter.get('temperature', 'NOT SET')}")
        print(f"Max Tokens:                {openrouter.get('max_tokens', 'NOT SET')}")

        # Scoring
        scoring = yaml_config.get('scoring', {})
        print(f"\nMin Qualified Score:       {scoring.get('min_qualified_score', 'NOT SET')}")

        # Logging
        logging_config = yaml_config.get('logging', {})
        print(f"\nLog Level:                 {logging_config.get('level', 'NOT SET')}")
        print(f"Log File:                  {logging_config.get('file', 'NOT SET')}")

    # Summary
    print("\n[3] Configuration Summary")
    print("-" * 60)

    env_complete = all(v != 'NOT SET' for v in env_config.values())
    yaml_complete = 'error' not in yaml_config

    if env_complete and yaml_complete:
        print("✓ All configuration values are set!")
        print("\nReady to run:")
        print("  python main.py --max-companies 2 --max-profiles 2  (test)")
        print("  python main.py                                      (full run)")
        print("  python main.py --schedule                           (scheduled)")
    else:
        print("✗ Configuration incomplete!")
        if not env_complete:
            print("  → Missing environment variables in .env")
        if not yaml_complete:
            print("  → Issues with config.yaml")
        print("\nSee SETUP_GUIDE.md for configuration instructions")

    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
