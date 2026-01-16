import requests

API_KEY = "0c1fad3977a3b907076ec014cbb4cf4e"
URL = "http://api.aviationstack.com/v1/flights"

print("Testing API key...")
print(f"Key: {API_KEY[:10]}...")

params = {'access_key': API_KEY}

response = requests.get(URL, params=params)
data = response.json()

print("\nResponse:")
print(data)

if 'error' in data:
    print(f"\n❌ API Error: {data['error']}")
else:
    print(f"\n✅ API works! Found {len(data.get('data', []))} flights")