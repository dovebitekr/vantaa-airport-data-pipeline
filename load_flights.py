import json
import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv

#Load pwd for the database
load_dotenv()

def load_data_to_db():
    """
    Loads the processed flight data from JSON into the PostgreSQL database.
    """
    # 1: Database connection parameters
    db_config = {
        "host": "localhost",
        "database": "postgres",
        "user": "postgres",
        "password": os.getenv("DB_PASSWORD"), 
        "port": "5432"
    }
    try:
            # Connect to an existing database
            connection = psycopg2.connect(**db_config)
            cursor = connection.cursor()
            print("Successfully connected to PostgreSQL!")

            # 2: Read the JSON file
            with open('vantaa_flights.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            states = data.get('states', [])
            collected_at = data.get('collected_at')

            if not states:
                print("No flight data found to insert.")
                return
            
            # 3: SQL Insert Query
            insert_query = """
                INSERT INTO vantaa_flights 
                (icao24, callsign, origin_country, longitude, latitude, baro_altitude, on_ground, collected_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # 4: Insert records one by one
            record_count = 0
            for flight in states:
                # Data Cleaning: Handle empty callsigns and preserve NULL altitudes
                callsign = flight[1].strip() if flight[1] else None
                altitude = flight[7] # Keep as None (NULL) if empty
                
                record_to_insert = (
                    flight[0],      # icao24
                    callsign,       # callsign
                    flight[2],      # origin_country
                    flight[5],      # longitude
                    flight[6],      # latitude
                    altitude,       # baro_altitude (Preserving NULL)
                    flight[8],      # on_ground
                    collected_at    # timestamp
                )
                
                cursor.execute(insert_query, record_to_insert)
                record_count += 1

            # 5: Commit the transaction
            connection.commit()
            print(f"Success! {record_count} flight records have been loaded into the database.")
        
    except (Exception, Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}")
    finally:
        # 6. Close the connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")

if __name__ == "__main__":
    load_data_to_db()