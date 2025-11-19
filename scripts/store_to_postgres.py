import pandas as pd
from sqlalchemy import create_engine
import os

DB_USER = "postgres"          
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password_here_if_local")
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "nyc_payroll_db"

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

print("✅ Connected to PostgreSQL!")

try:
    df = pd.read_json("raw/nyc_payroll_2025-11-18.json")
except ValueError:
    
    df = pd.read_csv("docs/NYC_Payroll_2025.csv")

print(f"📄 Loaded {len(df)} rows from file")

table_name = "staging_payroll"

df.to_sql(table_name, engine, if_exists="replace", index=False)
print(f"💾 Data successfully loaded into table '{table_name}' in PostgreSQL!")
