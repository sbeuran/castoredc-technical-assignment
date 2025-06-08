import requests
import json

BASE_URL = "https://fruits-api-app.azurewebsites.net"

def test_endpoints():
    # Test root endpoint first
    print("\nTesting root endpoint (/)...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    if response.ok:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")

    # Test basic fruits endpoint
    print("\nTesting /api/v1/fruits endpoint...")
    response = requests.get(f"{BASE_URL}/api/v1/fruits")
    print(f"Status: {response.status_code}")
    if response.ok:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")

    # Test extended data endpoint
    print("\nTesting /api/v1/get_all_data endpoint...")
    response = requests.get(f"{BASE_URL}/api/v1/get_all_data")
    print(f"Status: {response.status_code}")
    if response.ok:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_endpoints() 