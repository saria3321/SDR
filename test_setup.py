"""
Test Setup Script - Verify all configurations and connections
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def print_status(test_name, passed, message=""):
    """Print colored status"""
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status}: {test_name}")
    if message:
        print(f"       {message}")

def test_environment_variables():
    """Test if all required environment variables are set"""
    print("\n[1/6] Testing Environment Variables")
    print("-" * 50)

    required_vars = {
        'APIFY_API_TOKEN': 'Apify API token',
        'OPENROUTER_API_KEY': 'OpenRouter API key',
        'GOOGLE_SHEETS_CREDENTIALS_PATH': 'Google credentials path',
        'ICP_SHEET_ID': 'ICP Sheet ID',
        'OUTPUT_SHEET_ID': 'Output Sheet ID'
    }

    all_pass = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if 'KEY' in var or 'TOKEN' in var:
                display = value[:10] + "..." if len(value) > 10 else "***"
            else:
                display = value
            print_status(description, True, display)
        else:
            print_status(description, False, "Not set in .env")
            all_pass = False

    return all_pass

def test_credentials_file():
    """Test if Google credentials file exists"""
    print("\n[2/6] Testing Google Credentials File")
    print("-" * 50)

    creds_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH', 'credentials.json')
    exists = Path(creds_path).exists()

    print_status("Credentials file exists", exists, creds_path)

    if exists:
        try:
            import json
            with open(creds_path, 'r') as f:
                creds = json.load(f)

            has_key = 'client_email' in creds and 'private_key' in creds
            print_status("Valid credentials format", has_key,
                        f"Service account: {creds.get('client_email', 'N/A')}")
            return has_key
        except Exception as e:
            print_status("Valid credentials format", False, str(e))
            return False

    return False

def test_google_sheets_connection():
    """Test connection to Google Sheets"""
    print("\n[3/6] Testing Google Sheets Connection")
    print("-" * 50)

    try:
        import gspread
        from google.oauth2.service_account import Credentials

        creds_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
        icp_sheet_id = os.getenv('ICP_SHEET_ID')
        output_sheet_id = os.getenv('OUTPUT_SHEET_ID')

        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

        creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
        client = gspread.authorize(creds)

        # Test ICP sheet
        try:
            icp_sheet = client.open_by_key(icp_sheet_id)
            print_status("ICP Sheet accessible", True, icp_sheet.title)
        except Exception as e:
            print_status("ICP Sheet accessible", False, str(e))
            return False

        # Test output sheet
        try:
            output_sheet = client.open_by_key(output_sheet_id)
            print_status("Output Sheet accessible", True, output_sheet.title)
        except Exception as e:
            print_status("Output Sheet accessible", False, str(e))
            return False

        return True

    except Exception as e:
        print_status("Google Sheets connection", False, str(e))
        return False

def test_apify_connection():
    """Test Apify API connection"""
    print("\n[4/6] Testing Apify Connection")
    print("-" * 50)

    try:
        from apify_client import ApifyClient

        api_token = os.getenv('APIFY_API_TOKEN')
        client = ApifyClient(api_token)

        # Test by getting user info
        user = client.user().get()

        if user:
            print_status("Apify API connection", True, f"User: {user.get('username', 'N/A')}")
            return True
        else:
            print_status("Apify API connection", False, "Could not get user info")
            return False

    except Exception as e:
        print_status("Apify API connection", False, str(e))
        return False

def test_openrouter_connection():
    """Test OpenRouter API connection"""
    print("\n[5/6] Testing OpenRouter Connection")
    print("-" * 50)

    try:
        import openai

        api_key = os.getenv('OPENROUTER_API_KEY')
        client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

        # Test with a minimal request
        response = client.chat.completions.create(
            model="anthropic/claude-3.5-sonnet",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )

        if response.choices:
            print_status("OpenRouter API connection", True, "Successfully sent test request")
            return True
        else:
            print_status("OpenRouter API connection", False, "No response received")
            return False

    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "authentication" in error_msg.lower():
            print_status("OpenRouter API connection", False, "Invalid API key")
        elif "insufficient" in error_msg.lower() or "credit" in error_msg.lower():
            print_status("OpenRouter API connection", False, "Insufficient credits")
        else:
            print_status("OpenRouter API connection", False, error_msg)
        return False

def test_dependencies():
    """Test if all Python dependencies are installed"""
    print("\n[6/6] Testing Python Dependencies")
    print("-" * 50)

    dependencies = [
        'gspread',
        'google.auth',
        'apify_client',
        'openai',
        'pydantic',
        'yaml',
        'schedule'
    ]

    all_pass = True
    for dep in dependencies:
        try:
            __import__(dep.replace('.', '_'))
            print_status(f"{dep} installed", True)
        except ImportError:
            print_status(f"{dep} installed", False, "Run: pip install -r requirements.txt")
            all_pass = False

    return all_pass

def main():
    """Run all tests"""
    print("=" * 50)
    print("AI SDR - Setup Verification Test")
    print("=" * 50)

    # Load environment
    load_dotenv()

    # Run all tests
    results = {
        "Environment Variables": test_environment_variables(),
        "Credentials File": test_credentials_file(),
        "Google Sheets": test_google_sheets_connection(),
        "Apify": test_apify_connection(),
        "OpenRouter": test_openrouter_connection(),
        "Dependencies": test_dependencies()
    }

    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)

    passed = sum(results.values())
    total = len(results)

    for test, result in results.items():
        status = "✓" if result else "✗"
        print(f"{status} {test}")

    print("-" * 50)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("\n✓ All tests passed! You're ready to run the AI SDR system.")
        print("\nNext step: python main.py --max-companies 2 --max-profiles 2")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix the issues above.")
        print("\nRefer to SETUP_GUIDE.md for detailed instructions.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
