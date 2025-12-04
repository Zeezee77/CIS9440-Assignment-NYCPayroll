CREATE OR REPLACE TABLE nyc_payroll_dw.dim_agency AS
SELECT
  ROW_NUMBER() OVER (ORDER BY `Agency Name`, `Work Location Borough`) AS agency_id,
  `Agency Name` AS agency_name,
  `Work Location Borough` AS work_location_borough
FROM (
  SELECT DISTINCT
    `Agency Name`,
    `Work Location Borough`
  FROM nyc_payroll_dw.staging_payroll
)
ORDER BY agency_id;
