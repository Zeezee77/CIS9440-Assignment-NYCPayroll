CREATE OR REPLACE TABLE nyc_payroll_dw.fact_payroll AS
SELECT
  GENERATE_UUID() AS payroll_fact_id,

  a.agency_id,
  e.employee_id,
  t.title_id,
  d1.date_id AS payroll_date_id,
  d2.date_id AS start_date_id,

  SAFE_CAST(REGEXP_REPLACE(`Base Salary`, r'[^0-9.]', '') AS FLOAT64) AS base_salary,
  SAFE_CAST(REGEXP_REPLACE(`Regular Hours`, r'[^0-9.]', '') AS FLOAT64) AS regular_hours,
  SAFE_CAST(REGEXP_REPLACE(`Regular Gross Paid`, r'[^0-9.]', '') AS FLOAT64) AS regular_gross_paid,
  SAFE_CAST(REGEXP_REPLACE(`OT Hours`, r'[^0-9.]', '') AS FLOAT64) AS ot_hours,
  SAFE_CAST(REGEXP_REPLACE(`Total OT Paid`, r'[^0-9.]', '') AS FLOAT64) AS total_ot_paid,
  SAFE_CAST(REGEXP_REPLACE(`Total Other Pay`, r'[^0-9.]', '') AS FLOAT64) AS total_other_pay

FROM nyc_payroll_dw.staging_payroll s
JOIN nyc_payroll_dw.dim_agency a
  ON s.`Agency Name` = a.agency_name
 AND s.`Work Location Borough` = a.work_location_borough
JOIN nyc_payroll_dw.dim_employee e
  ON s.`First Name` = e.first_name
 AND s.`Last Name`  = e.last_name
 AND s.`Mid Init`   = e.middle_initial
JOIN nyc_payroll_dw.dim_title t
  ON s.`Title Description` = t.title_description
JOIN nyc_payroll_dw.dim_date d1
  ON d1.full_date = DATE(PARSE_DATE('%m/%d/%Y', s.`Agency Start Date`))
JOIN nyc_payroll_dw.dim_date d2
  ON d2.full_date = PARSE_DATE('%m/%d/%Y', s.`Agency Start Date`);
