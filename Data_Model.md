## 🧱 Data Model (Data Warehouse)

**Fact Table:** `dw.fact_payroll`  
Contains detailed payroll payment records by employee, agency, and fiscal year.

| Column | Description | Type | Example |
|--------|--------------|------|----------|
| fiscal_year | Fiscal year of payroll record | INT | 2025 |
| agency_name | NYC Agency name | TEXT | HRA/Dept of Social Services |
| title_description | Employee job title | TEXT | CASEWORKER |
| base_salary | Base salary amount | FLOAT | 55000.00 |
| pay_basis | Pay frequency (per annum, per diem, etc.) | TEXT | per Annum |
| employee_name | Full name (First + Middle + Last) | TEXT | ALEXIS MAJOR |

**Dimensions:**
- **Agency Dimension:** agency_name, related attributes  
- **Employee Dimension:** employee_name, title_description  
- **Time Dimension:** fiscal_year  

**Grain:**  
Each record in the fact table represents one employee’s payroll record for one fiscal year.
