import functions_framework
from google.cloud import bigquery, storage
import pandas as pd
import pyarrow
import os
import json

# ---------------------------
# CONFIGURATION
# ---------------------------
PROJECT_ID = "superb-ethos-480103-b6"
DATASET = "nyc_payroll_dw"
BUCKET_NAME = "nyc-payroll-bucket-2025"   # <-- replace with your bucket
FILE_NAME = "NYC_Payroll_2025.csv"        # <-- replace if different

# Initialize clients
bq_client = bigquery.Client()
storage_client = storage.Client()


# ---------------------------
# MAIN ELT FUNCTION (Cloud Run Entry Point)
# ---------------------------
@functions_framework.http
def run_elt(request):

    try:
        # 1. Load CSV from GCS
        df = load_from_gcs(BUCKET_NAME, FILE_NAME)

        # 2. Load dataframe → staging table
        staging_rows = load_to_bigquery(df)

        # 3. Execute SQL build steps
        build_dim_tables()
        build_fact_table()

        return json.dumps({
            "status": "success",
            "staging_rows_loaded": staging_rows,
            "message": "ELT pipeline completed successfully."
        }), 200

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        }), 500


# ---------------------------
# LOAD RAW DATA FROM GCS
# ---------------------------
def load_from_gcs(bucket_name, file_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    data = blob.download_as_text()
    df = pd.read_csv(pd.compat.StringIO(data))

    print(f"📥 Loaded {len(df)} rows from GCS")
    return df


# ---------------------------
# LOAD STAGING TABLE IN BIGQUERY
# ---------------------------
def load_to_bigquery(df):

    table_id = f"{PROJECT_ID}.{DATASET}.staging_payroll"

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
    )

    job = bq_client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()

    print(f"📌 Loaded {job.output_rows} rows into staging table.")
    return job.output_rows


# ---------------------------
# RUN DIMENSION TABLE SCRIPTS
# ---------------------------
def build_dim_tables():

    dim_queries = [
        "sql/create_dim_agency.sql",
        "sql/create_dim_employee.sql",
        "sql/create_dim_title.sql",
        "sql/create_dim_date.sql"
    ]

    for script in dim_queries:
        execute_sql_file(script)
        print(f"✅ Built: {script}")


# ---------------------------
# RUN FACT TABLE SCRIPT
# ---------------------------
def build_fact_table():

    script = "sql/create_fact_payroll.sql"
    execute_sql_file(script)
    print("📊 Fact table created.")


# ---------------------------
# HELPER: Execute SQL file
# ---------------------------
def execute_sql_file(filepath):

    with open(filepath, "r") as f:
        query = f.read()

    job = bq_client.query(query)
    job.result()
