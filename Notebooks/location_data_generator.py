import pandas as pd
import json
import os

# Define the comprehensive list provided by the user
LOCATION_LIST = [
    "Kukatpally", "Miyapur", "Nallagandla", "Narsingi", "Uppal", 
    "Punjagutta", "Kollur", "Rajendra Nagar", "Nizampet", "Begumpet", 
    "Attapur", "Somajiguda", "Patancheru", "LB Nagar", "Bachupally", 
    "Hitech City", "Rampally", "Mehdipatnam", "Banjara Hills", "Kompally", 
    "Gachibowli", "Pocharam", "Ameerpet", "Tolichowki", "Kondapur", 
    "Secunderabad", "Jubilee Hills", "Shamshabad", "Manikonda", "Madhapur"
]

STATIC_DIR = 'static'
OUTPUT_FILE = os.path.join(STATIC_DIR, 'location_suggestions.json')
os.makedirs(STATIC_DIR, exist_ok=True)

# Sort the list alphabetically for better user experience
LOCATION_LIST.sort()

try:
    # Save the list to the JSON file
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(LOCATION_LIST, f, indent=4)
    
    print(f"Successfully updated {len(LOCATION_LIST)} unique locations in {OUTPUT_FILE}")
except Exception as e:
    print(f"Error saving location data: {e}")