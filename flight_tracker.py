import requests
import pandas as pd
from datetime import datetime
import os

# ============ CONFIG (INLINE) ============
AVIATION_API_KEY = "0c1fad3977a3b907076ec014cbb4cf4e"
BASE_URL = "http://api.aviationstack.com/v1/flights"
DATA_FOLDER = "data"

DOMESTIC_ROUTES = [
    {"from": "DFW", "to": "LAX", "name": "DFW to Los Angeles", "type": "domestic"},
    {"from": "DFW", "to": "JFK", "name": "DFW to New York", "type": "domestic"},
    {"from": "DFW", "to": "ORD", "name": "DFW to Chicago", "type": "domestic"}
]

INTERNATIONAL_ROUTES = [
    {"from": "DFW", "to": "LHR", "name": "DFW to London", "type": "international"},
    {"from": "DFW", "to": "MEX", "name": "DFW to Mexico City", "type": "international"}
]

# ============ FUNCTIONS ============

def fetch_flight_data(origin, destination):
    print(f"  Fetching flights from {origin} to {destination}...")
    
    params = {
        'access_key': AVIATION_API_KEY,
        'dep_iata': origin,
        'arr_iata': destination
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        print(f"  Response status: {response.status_code}")  # Add this
        print(f"  Response text: {response.text[:500]}")  # Add this (first 500 chars)
        data = response.json()
        
        if 'data' in data and len(data['data']) > 0:
            print(f"  ✅ Found {len(data['data'])} flights!")
            return data['data']
        else:
            print("  ⚠️ No flights found (check API response above)")
            return []
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return []

def parse_flight_data(flights, route_info):
    parsed_flights = []
    
    for flight in flights:
        try:
            flight_info = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'time': datetime.now().strftime('%H:%M:%S'),
                'route': route_info['name'],
                'route_type': route_info['type'],
                'origin': route_info['from'],
                'destination': route_info['to'],
                'flight_number': flight.get('flight', {}).get('iata', 'N/A'),
                'airline': flight.get('airline', {}).get('name', 'N/A'),
                'status': flight.get('flight_status', 'N/A'),
            }
            parsed_flights.append(flight_info)
        except:
            continue
    
    return parsed_flights

def save_to_csv(data, filename):
    if not data:
        return
    
    os.makedirs(DATA_FOLDER, exist_ok=True)
    filepath = os.path.join(DATA_FOLDER, filename)
    
    df = pd.DataFrame(data)
    
    if os.path.exists(filepath):
        existing_df = pd.read_csv(filepath)
        df = pd.concat([existing_df, df], ignore_index=True)
        print(f"  ✅ Appended to {filename}")
    else:
        print(f"  ✅ Created {filename}")
    
    df.to_csv(filepath, index=False)

def process_routes(routes, label):
    collected = []
    
    print(f"\n{label}")
    print("="*70)
    
    for route in routes:
        print(f"\n📍 {route['name']}")
        
        flights = fetch_flight_data(route['from'], route['to'])
        
        if flights:
            parsed = parse_flight_data(flights, route)
            collected.extend(parsed)
            
            filename = f"{route['type']}_{route['from']}_{route['to']}.csv"
            save_to_csv(parsed, filename)
    
    return collected

def main():
    print("="*70)
    print("✈️  DFW FLIGHT TRACKER")
    print("="*70)
    
    domestic = process_routes(DOMESTIC_ROUTES, "🇺🇸 DOMESTIC FLIGHTS")
    international = process_routes(INTERNATIONAL_ROUTES, "🌍 INTERNATIONAL")
    
    print(f"\n📊 TOTAL: {len(domestic) + len(international)} flights collected")
    print("="*70)

if __name__ == "__main__":
    main()