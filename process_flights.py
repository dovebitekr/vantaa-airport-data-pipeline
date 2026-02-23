import json

def clean_and_filter_data():
    # preprocessing raw JSON data
    
    try:
        # 1: Read the raw data file 
        with open('vantaa_flights.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
    except FileNotFoundError:
        print("Error: Could not find 'vantaa_flights.json'. Please run get_flights.py first.")
        return

    states = data.get('states', [])
    if not states:
        print("No flights to process.")
        return
        
    # 2: Print Header
    print(f"\n--- Flight Data near Helsinki-Vantaa (Collected: {data.get('collected_at')}) ---")
    print(f"{'Callsign':<10} | {'Country':<15} | {'Altitude':<15} | {'Status':<10}")
    print("-" * 58)
    
    # 3: Process each flight
    for flight in states:
        # OpenSky API Index Mapping
        # [1] Callsign, [2] Origin Country, [7] Altitude, [8] On Ground status
        callsign = flight[1].strip() if flight[1] else "UNKNOWN"
        country = flight[2]
        altitude = flight[7]
        on_ground = flight[8]
        
        #Preserve Nulls
        alt_display = "NULL" if altitude is None else f"{altitude} m"
        
        status = "Landed" if on_ground else "In Air"

        #Print the cleaned data row
        print(f"{callsign:<10} | {country:<15} | {alt_display:<15} | {status:<10}")

if __name__ == "__main__":
    clean_and_filter_data()