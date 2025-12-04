CREATE OR REPLACE TABLE nyc_payroll_dw.fact_payroll AS
SELECT
  GENERATE_UUID() AS payroll_fact_id,

  -- Foreign keys to dimensions
  a.agency_id,
  e.employee_id,
  t.title_id,

  -- Two role-playing date dimension keys
  pd.date_id AS payroll_date_id,
  sd.date_id AS start_date_id,

  -- Measures
  SAFE_CAST(s.`Base Salary` AS FLOAT64) AS base_salary,
  SAFE_CAST(s.`Regular Hours` AS FLOAT64) AS regular_hours,
  SAFE_CAST(s.`Regular Gross Paid` AS FLOAT64) AS regular_gross_paid,
  SAFE_CAST(s.`OT Hours` AS FLOAT64) AS ot_hours,
  SAFE_CAST(s.`Total OT Paid` AS FLOAT64) AS total_ot_paid,
  SAFE_CAST(s.`Total Other Pay` AS FLOAT64) AS total_other_pay

FROM nyc_payroll_dw.staging_payroll s

JOIN nyc_payroll_dw.dim_agency a
  ON s.`Agency Name` = a.agency_name
 AND s.`Work Location Borough` = a.work_location_borough

JOIN nyc_payroll_dw.dim_employee e
  ON s.`First Name` = e.first_name
 AND s.`Last Name` = e.last_name
 AND s.`Mid Init` = e.middle_initial

JOIN nyc_payroll_dw.dim_title t
  ON s.`Title Description` = t.title_description

-- Payroll Date (Fiscal Year ends June 30)
JOIN nyc_payroll_dw.dim_date pd
  ON pd.full_date = DATE(s.`Fiscal Year`, 6, 30)

-- Employee Start Date
JOIN nyc_payroll_dw.dim_date sd
  ON sd.full_date = PARSE_DATE('%m/%d/%Y', s.`Agency Start Date`);
