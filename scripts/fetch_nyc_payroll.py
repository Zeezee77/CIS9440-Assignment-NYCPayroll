import requests, json, datetime, pathlib


BASE_URL = "https://data.cityofnewyork.us/resource/k397-673e.json"


PARAMS = {"$limit": 50000}

print("📡 Fetching data from NYC Open Data API...")
response = requests.get(BASE_URL, params=PARAMS)

if response.status_code == 200:
    data = response.json()
    print(f"✅ Retrieved {len(data)} records")

    raw_dir = pathlib.Path("raw")
    raw_dir.mkdir(exist_ok=True)
    filename = raw_dir / f"nyc_payroll_{datetime.date.today()}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"💾 Data saved to {filename}")
else:
    print(f"❌ Error fetching data: {response.status_code} - {response.text}")
