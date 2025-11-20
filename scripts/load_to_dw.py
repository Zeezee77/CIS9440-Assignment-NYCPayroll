import pandas as pd
from sqlalchemy import create_engine, text
import os

DB_USER = "postgres"
DB_PASSWORD = "Withtheclouds7"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "nyc_payroll_db"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("✅ Connected to PostgreSQL (DW phase)")

with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS dw;"))
    conn.commit()

df = pd.read_sql("SELECT * FROM staging_payroll", engine)
print(f"📦 Loaded {len(df)} rows from staging_payroll")

dim_agency = df[["agency_name", "work_location_borough"]].drop_duplicates()
dim_agency["agency_id"] = range(1, len(dim_agency) + 1)

dim_employee = df[
    ["first_name", "mid_init", "last_name", "title_description", "leave_status_as_of_june_30"]
].drop_duplicates()
dim_employee["employee_id"] = range(1, len(dim_employee) + 1)

dim_pay = df[["pay_basis", "regular_hours"]].drop_duplicates()
dim_pay["pay_id"] = range(1, len(dim_pay) + 1)

dim_time = df[["fiscal_year", "payroll_number", "agency_start_date"]].drop_duplicates()
dim_time["time_id"] = range(1, len(dim_time) + 1)


dim_agency.to_sql("dim_agency", engine, schema="dw", if_exists="replace", index=False)
dim_employee.to_sql("dim_employee", engine, schema="dw", if_exists="replace", index=False)
dim_pay.to_sql("dim_pay", engine, schema="dw", if_exists="replace", index=False)
dim_time.to_sql("dim_time", engine, schema="dw", if_exists="replace", index=False)

print("📚 Dimensions loaded successfully.")

merged = (
    df.merge(dim_agency, on=["agency_name", "work_location_borough"])
      .merge(dim_employee, on=["first_name", "mid_init", "last_name", "title_description", "leave_status_as_of_june_30"])
      .merge(dim_pay, on=["pay_basis", "regular_hours"])
      .merge(dim_time, on=["fiscal_year", "payroll_number", "agency_start_date"])
)

fact = merged[
    [
        "agency_id",
        "employee_id",
        "time_id",
        "pay_id",
        "base_salary",
        "regular_gross_paid",
        "ot_hours",
        "total_ot_paid",
        "total_other_pay"
    ]
]


fact.to_sql("fact_payroll", engine, schema="dw", if_exists="replace", index=False)

print(f"💾 Loaded {len(fact)} rows into dw.fact_payroll")
print("🎯 Data warehouse (star schema) successfully built!")
