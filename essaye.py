from pathlib import Path

DATA_FOLDER = Path("data")
DATA_FOLDER.mkdir(exist_ok=True)

file_path = DATA_FOLDER / "test.csv"
print(not file_path.exists())

with open(file_path, "a") as f:
    pass

print(not file_path.exists())

COLUMNS = ["timestamp_utc", "station_id", "docks_available"]

rows = [
    {"timestamp_utc": "2026-10-29T18:28:43Z", "station_id": "1024", "docks_available": 11},
    {"timestamp_utc": "2026-10-29T18:28:43Z", "station_id": "20004", "docks_available": 3},
]


