"""
Test Apify Actor - Verify the LinkedIn scraper works
"""
import os
from dotenv import load_dotenv
from apify_client import ApifyClient

# Load environment
load_dotenv()

def test_apify_actor():
    """Test the Apify LinkedIn actor"""
    print("=" * 60)
    print("Testing Apify LinkedIn Actor")
    print("=" * 60)

    api_token = os.getenv('APIFY_API_TOKEN')

    if not api_token:
        print("❌ ERROR: APIFY_API_TOKEN not found in .env")
        return

    print(f"\n✓ API Token found: {api_token[:10]}...")

    # Create client
    client = ApifyClient(api_token)

    # Test the recommended actor
    actor_id = "harvestapi/linkedin-profile-search"

    print(f"\n📋 Testing Actor: {actor_id}")
    print("-" * 60)

    # Simple test input
    run_input = {
        "search": "CEO software France",
        "locations": ["France"],
        "maxResults": 3,  # Small test
    }

    print(f"\n🔍 Search Input:")
    print(f"  Search: {run_input['search']}")
    print(f"  Locations: {run_input['locations']}")
    print(f"  Max Results: {run_input['maxResults']}")

    try:
        print("\n⏳ Running actor (this may take 30-60 seconds)...")
        run = client.actor(actor_id).call(run_input=run_input)

        print(f"\n✓ Actor run completed!")
        print(f"  Run ID: {run['id']}")
        print(f"  Status: {run['status']}")

        # Get results
        dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items

        print(f"\n✅ SUCCESS! Got {len(dataset_items)} results")

        if dataset_items:
            print("\n" + "=" * 60)
            print("SAMPLE RESULT (First Profile):")
            print("=" * 60)

            first_result = dataset_items[0]

            # Show key fields
            print(f"\nName: {first_result.get('fullName') or first_result.get('name', 'N/A')}")
            print(f"Title: {first_result.get('title') or first_result.get('headline', 'N/A')}")
            print(f"Location: {first_result.get('location', 'N/A')}")
            print(f"LinkedIn URL: {first_result.get('profileUrl') or first_result.get('url', 'N/A')}")

            print("\n" + "-" * 60)
            print("All Available Fields:")
            print("-" * 60)
            for key in sorted(first_result.keys()):
                value = str(first_result[key])[:50]  # First 50 chars
                print(f"  {key}: {value}")

            print("\n" + "=" * 60)
            print("✅ ACTOR WORKS! You can use this actor.")
            print("=" * 60)

            print("\n📝 Next Steps:")
            print("1. Update your .env file:")
            print(f"   APIFY_COMPANY_SCRAPER_ACTOR={actor_id}")
            print(f"   APIFY_EMPLOYEE_SCRAPER_ACTOR={actor_id}")
            print("\n2. Run the simplified version:")
            print("   python main_simplified.py --max-companies 2 --max-profiles 2")

        else:
            print("\n⚠️  No results returned. Try different search criteria.")

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check your Apify API token is correct")
        print("2. Make sure you have credits in your Apify account")
        print("3. Try a different actor from Apify store")
        print("4. Visit https://apify.com/store to find LinkedIn scrapers")

if __name__ == "__main__":
    test_apify_actor()
