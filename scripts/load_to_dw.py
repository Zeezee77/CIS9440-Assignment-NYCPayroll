import pandas as pd
from sqlalchemy import create_engine, text
import os 

DB_USER = "postgres"
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password_here_if_local") 
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "nyc_payroll_db"

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
print("✅ Connected to PostgreSQL (DW phase)")

# Ensure schema exists
with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS dw;"))
    conn.commit()


df = pd.read_sql("SELECT * FROM staging_payroll", engine)
print(f"📦 Loaded {len(df)} rows from staging_payroll")
print("🧱 Available columns:", list(df.columns))


if all(col in df.columns for col in ["first_name", "last_name"]):
    df["employee_name"] = (
        df["first_name"].fillna("") + " " +
        df.get("mid_init", "").fillna("") + " " +
        df["last_name"].fillna("")
    ).str.strip()
else:
    df["employee_name"] = ""  

columns = [
    "fiscal_year",
    "agency_name",
    "title_description",
    "base_salary",
    "pay_basis",
    "employee_name"
]


df_dw = df[[c for c in columns if c in df.columns]].copy()


df_dw.to_sql(
    name="fact_payroll",
    con=engine,
    schema="dw",
    if_exists="replace",
    index=False
)

print(f"💾 Loaded {len(df_dw)} records into dw.fact_payroll")
print("🎯 Fact table now reflects HRA/Dept of Social Services FY2025 dataset.")
