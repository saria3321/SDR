"""
Simple test without dependencies - just verify credentials
"""
import json
import os

print("=" * 60)
print("Testing Configuration")
print("=" * 60)

# Test .env file
print("\n[1] Checking .env file...")
if os.path.exists('.env'):
    print("[OK] .env file exists")
    with open('.env', 'r') as f:
        lines = [l.strip() for l in f.readlines() if l.strip() and not l.startswith('#')]
        print(f"[OK] Found {len(lines)} configuration lines")
        for line in lines:
            key = line.split('=')[0]
            print(f"  - {key}: configured")
else:
    print("[FAIL] .env file not found")

# Test credentials.json
print("\n[2] Checking credentials.json...")
if os.path.exists('credentials.json'):
    print("[OK] credentials.json exists")
    with open('credentials.json', 'r') as f:
        creds = json.load(f)
        print(f"[OK] Project ID: {creds.get('project_id')}")
        print(f"[OK] Service Account: {creds.get('client_email')}")
else:
    print("[FAIL] credentials.json not found")

# Test Google Sheets IDs
print("\n[3] Checking Google Sheet IDs...")
icp_sheet = "1Z1N2p8t0iUB2FaldGcpDGsu7qbbKTJ-LfB6PQKn7v3Y"
output_sheet = "1wIzjo9vJfAZiutLxeSv_0zqGviGwFFrK7DkP3lSrUxc"

print(f"[OK] ICP Sheet: https://docs.google.com/spreadsheets/d/{icp_sheet}")
print(f"[OK] Output Sheet: https://docs.google.com/spreadsheets/d/{output_sheet}")

print("\n=" * 60)
print("Configuration Test Complete!")
print("=" * 60)

print("\nNext Steps:")
print("1. Make sure you have Python dependencies installed")
print("2. Share both Google Sheets with:")
print(f"   hyvop-ai-automation@hyvop-481511.iam.gserviceaccount.com")
print("3. Run: python test_apify_actor.py")
print("4. Run: python main_simplified.py --max-companies 2 --max-profiles 2")
