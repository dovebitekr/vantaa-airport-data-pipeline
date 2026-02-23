import requests
import json
import os
from datetime import datetime

#Helsinki-Vantaa Airport area coordinates
FINLAND_BOUNDS = {
    "lamin": 60.1,
    "lomin": 24.5,
    "lamax": 60.5,
    "lomax": 25.5
}

def fetch_and_save_flights():
    url = "https://opensky-network.org/api/states/all"
    print(f"[{datetime.now()}] Starting data collection...")
    
    try:
        # Requesting data from OpenSky API
        response = requests.get(url, params=FINLAND_BOUNDS)
        
        if response.status_code == 200:
            raw_data = response.json()
            
            # 2. Data Processing: Add timestamp to the data
            raw_data['collected_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 3. Storage: Save the data as a JSON file
            filename = "vantaa_flights.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(raw_data, f, indent=4)
                
            print(f"Successfully saved data to {filename}")
            print(f"Flights found: {len(raw_data['states']) if raw_data['states'] else 0}")
            
        else:
            print(f"API Error: Received status code {response.status_code}")
            
    except Exception as e:
        print(f"Critical Error: {str(e)}")

if __name__ == "__main__":
    fetch_and_save_flights()