CREATE OR REPLACE TABLE nyc_payroll_dw.dim_employee AS
SELECT
  ROW_NUMBER() OVER (ORDER BY `First Name`, `Last Name`, `Mid Init`) AS employee_id,
  `First Name` AS first_name,
  `Mid Init` AS middle_initial,
  `Last Name` AS last_name
FROM (
  SELECT DISTINCT
    `First Name`, 
    `Mid Init`, 
    `Last Name`
  FROM nyc_payroll_dw.staging_payroll
)
ORDER BY employee_id;
