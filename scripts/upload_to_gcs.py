import os
from google.cloud import storage

# -----------------------------
# Configuration
# -----------------------------
BUCKET_NAME = "nyc-payroll-2025"   # <-- change to your bucket name
LOCAL_FILE = "raw/NYC_Payroll_2025.csv"
DESTINATION_BLOB = "raw/NYC_Payroll_2025.csv"

# -----------------------------
# Upload Function
# -----------------------------
def upload_file_to_gcs(bucket_name, source_file, destination_blob):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)

    blob.upload_from_filename(source_file)
    print(f"✅ Uploaded {source_file} → gs://{bucket_name}/{destination_blob}")


# -----------------------------
# Main Script
# -----------------------------
if __name__ == "__main__":
    print("🚀 Uploading NYC Payroll dataset to Google Cloud Storage...")
    upload_file_to_gcs(BUCKET_NAME, LOCAL_FILE, DESTINATION_BLOB)
    print("🎉 Upload completed.")
