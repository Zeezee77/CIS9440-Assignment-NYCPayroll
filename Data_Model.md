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

| **Dimension** | **Key Attributes** | **Description** |
|----------------|--------------------|-----------------|
| **Agency Dimension** | `agency_name` | Contains agency details such as name and related attributes |
| **Employee Dimension** | `employee_name`, `title_description` | Represents unique employees and their job titles |
| **Time Dimension** | `fiscal_year` | Represents fiscal year for payroll data |

---

### **Grain**
Each record in the fact table represents **one employee’s payroll record for one fiscal year**.

---

### **Notes**
- **Data Source:** [NYC Open Data – Citywide Payroll Data (Fiscal Year)](https://data.cityofnewyork.us/resource/k397-673e.json)
- **Agency Filter:** HRA/Dept of Social Services  
- **Fiscal Year:** 2025