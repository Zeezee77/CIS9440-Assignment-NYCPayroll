CREATE OR REPLACE TABLE nyc_payroll_dw.dim_title AS
SELECT
  ROW_NUMBER() OVER (ORDER BY `Title Description`) AS title_id,
  `Title Description` AS title_description,
  `Leave Status as of June 30` AS leave_status
FROM (
  SELECT DISTINCT
    `Title Description`,
    `Leave Status as of June 30`
  FROM nyc_payroll_dw.staging_payroll
)
ORDER BY title_id;
