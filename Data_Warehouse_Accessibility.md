## 🔐 Data Warehouse Accessibility

The Data Warehouse (`nyc_payroll_db`) is fully created, populated, and verified using Python scripts — **not** through GUI clients such as DataGrip or DbSchema.

All data loading, transformation, and verification steps are executed **programmatically** as part of the ETL process:

| **Script** | **Description** |
|-------------|----------------|
| `scripts/fetch_nyc_payroll.py` | Fetches raw HRA/Dept of Social Services payroll data (FY2025) from the NYC Open Data API |
| `scripts/store_to_postgres.py` | Creates the staging table (`staging_payroll`) and loads the raw JSON data into PostgreSQL |
| `scripts/load_to_dw.py` | Creates the data warehouse schema (`dw`) and loads the cleaned data into `dw.fact_payroll` |

### **Access Instructions**
1. Clone this repository from GitHub  
2. Ensure PostgreSQL and required Python packages are installed (`pip install -r requirements.txt`)  
3. Run the ETL scripts in sequence:
   ```bash
   python scripts/fetch_nyc_payroll.py
   python scripts/store_to_postgres.py
   python scripts/load_to_dw.py
