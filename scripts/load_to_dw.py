import pandas as pd
from sqlalchemy import create_engine, text

DB_USER = "postgres"
DB_PASSWORD = "Withtheclouds7"  
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "nyc_payroll_db"

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

print("✅ Connected to PostgreSQL (DW phase)")

with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS dw;"))
    conn.commit()

df = pd.read_sql("SELECT * FROM staging_payroll", engine)
print(f"📦 Loaded {len(df)} rows from staging_payroll")

columns = [
    "fiscal_year",
    "agency_name",
    "title_description",
    "base_salary",
    "pay_basis",
    "first_name",
    "last_name",
    "mid_init"
]
df_dw = df[columns].copy()


df_dw["employee_name"] = (
    df_dw["first_name"].fillna("") + " " +
    df_dw["mid_init"].fillna("") + " " +
    df_dw["last_name"].fillna("")
).str.strip()


df_dw = df_dw.drop(columns=["first_name", "last_name", "mid_init"])


df_dw.columns = [
    "fiscal_year",
    "agency_name",
    "title_description",
    "base_salary",
    "pay_basis",
    "employee_name"
]

table_name = "dw.fact_payroll"

df_dw.to_sql(
    name="fact_payroll",
    con=engine,
    schema="dw",
    if_exists="replace",
    index=False
)

print(f"💾 Loaded {len(df_dw)} records into dw.fact_payroll")