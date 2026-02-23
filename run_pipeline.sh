#!/bin/bash

#Pipeline starts
echo "Starting HEL(Vantaa) Flight Data Pipeline."

#Data from API to Json
echo "Extracting data from OpenSky API."
python get_flights.py

#Load data to SQL
echo "Loading data into PostgreSQL."
python load_flights.py

#Finish
echo "Pipeline execution completed successfully!"