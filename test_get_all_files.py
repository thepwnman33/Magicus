import requests

# Replace the base URL with your Flask app's URL if different
BASE_URL = "http://127.0.0.1:5000"

response = requests.get(f"{BASE_URL}/get_all_files")

if response.status_code == 200:
    print("Received response from the server:")
    print(response.json())
else:
    print(f"Request failed with status code: {response.status_code}")
