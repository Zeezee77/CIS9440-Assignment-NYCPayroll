import requests
import json
from datetime import date
import os

URL = "https://data.cityofnewyork.us/resource/k397-673e.json"

os.makedirs("raw", exist_ok=True)
params = {
    "$limit": 50000,
    "$select": "fiscal_year,payroll_number,agency_name,last_name,first_name,mid_init,agency_start_date,work_location_borough,title_description,leave_status_as_of_june_30,base_salary,pay_basis,regular_hours,regular_gross_paid,ot_hours,total_ot_paid,total_other_pay",
    "$where": "fiscal_year=2025 AND agency_name='HRA/DEPT OF SOCIAL SERVICES'"
}

print("📡 Fetching data from NYC Open Data API (HRA/DEPT OF SOCIAL SERVICES FY2025)...")

response = requests.get(URL, params=params)

if response.status_code == 200:
    data = response.json()
    print(f"✅ Retrieved {len(data)} records")

    filename = f"raw/nyc_payroll_{date.today()}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"💾 Data saved to {filename}")
else:
    print(f"❌ API request failed: {response.status_code} - {response.text}")
