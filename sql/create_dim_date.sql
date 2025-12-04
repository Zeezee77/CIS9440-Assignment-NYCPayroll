CREATE OR REPLACE TABLE nyc_payroll_dw.dim_date AS
WITH calendar AS (
  SELECT
    day AS full_date,
    EXTRACT(YEAR FROM day) AS year,
    EXTRACT(QUARTER FROM day) AS quarter,
    EXTRACT(MONTH FROM day) AS month,
    FORMAT_DATE('%B', day) AS month_name,
    EXTRACT(DAY FROM day) AS day,
    EXTRACT(DAYOFWEEK FROM day) AS day_of_week,
    FORMAT_DATE('%A', day) AS day_name,
    EXTRACT(WEEK FROM day) AS week_number
  FROM UNNEST(GENERATE_DATE_ARRAY('2015-01-01', '2030-12-31', INTERVAL 1 DAY)) AS day
)
SELECT
  ROW_NUMBER() OVER (ORDER BY full_date) AS date_id,
  *
FROM calendar
ORDER BY full_date;
