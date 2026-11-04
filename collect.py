import requests

import time 
 
from datetime import datetime, timezone 
 
from pathlib import Path
 
import csv 
 
URL = "https://download.data.grandlyon.com/files/rdata/jcd_jcdecaux.jcdvelov/station_status.json"
 
COLUMNS = [
    "timestamp_utc",
    "station_id",
    "mechanical_bikes_available",
    "electric_bikes_available",
    "bikes_out_of_service",
    "docks_available",
    "docks_out_of_service",
    "can_rent",
    "can_return",
    "last_reported_utc",
]
 


for attempt in range(3):
    try:
        reponse = requests.get(URL, timeout=30)
        reponse.raise_for_status()
        break
    except requests.RequestException:
        if attempt == 2:
            raise
        time.sleep(10)
 
content = reponse.json() 
 
stations = content["data"]["stations"]
 
stations_active = [] 
 
for station in stations:
    if station["is_installed"]:
        stations_active.append(station)
 
 
def count_bikes(station,bike_type):
    for vehicle in station["vehicle_types_available"]:
        if vehicle["vehicle_type_id"] == bike_type :
            return vehicle["count"] 
    return 0 
 
 
def to_utc(secondes):
    return datetime.fromtimestamp(secondes, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
 
 
def station_to_row(station, timestamp_utc):
    return {
        "timestamp_utc": timestamp_utc,
        "station_id": station["station_id"],
        "mechanical_bikes_available": count_bikes(station, "mechanical"),
        "electric_bikes_available": count_bikes(station, "electrical"),
        "bikes_out_of_service": station["num_bikes_disabled"],
        "docks_available": station["num_docks_available"],
        "docks_out_of_service": station["num_docks_disabled"],
        "can_rent": int(station["is_renting"]),
        "can_return": int(station["is_returning"]),
        "last_reported_utc": to_utc(station["last_reported"]),
    }
 
timestamp_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
 
rows = [station_to_row(station, timestamp_utc) for station in stations_active]
 
DATA_FOLDER = Path("data")
file_path = DATA_FOLDER / f"{timestamp_utc[:10]}.csv"
DATA_FOLDER.mkdir(exist_ok=True)
is_new_file = not file_path.exists()
with open(file_path, "a", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=COLUMNS)
    if is_new_file:
        writer.writeheader()
    writer.writerows(rows) 
 
print(f"{timestamp_utc}: {len(rows)} stations saved to {file_path}")