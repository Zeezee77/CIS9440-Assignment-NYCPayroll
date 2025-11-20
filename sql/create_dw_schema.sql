CREATE SCHEMA IF NOT EXISTS nyc_payroll_dw;

CREATE TABLE IF NOT EXISTS nyc_payroll_dw.dim_agency (
    agency_id SERIAL PRIMARY KEY,
    agency_name TEXT,
    work_location_borough TEXT
);

CREATE TABLE IF NOT EXISTS nyc_payroll_dw.dim_employee (
    employee_id SERIAL PRIMARY KEY,
    first_name TEXT,
    mid_init TEXT,
    last_name TEXT,
    title_description TEXT,
    leave_status_as_of_june_30 TEXT
);

CREATE TABLE IF NOT EXISTS nyc_payroll_dw.dim_pay (
    pay_id SERIAL PRIMARY KEY,
    pay_basis TEXT,
    regular_hours NUMERIC
);

CREATE TABLE IF NOT EXISTS nyc_payroll_dw.dim_time (
    time_id SERIAL PRIMARY KEY,
    fiscal_year INT,
    payroll_number INT,
    agency_start_date DATE
);

CREATE TABLE IF NOT EXISTS nyc_payroll_dw.fact_payroll (
    payroll_id SERIAL PRIMARY KEY,

    agency_id INT REFERENCES nyc_payroll_dw.dim_agency(agency_id),
    employee_id INT REFERENCES nyc_payroll_dw.dim_employee(employee_id),
    time_id INT REFERENCES nyc_payroll_dw.dim_time(time_id),
    pay_id INT REFERENCES nyc_payroll_dw.dim_pay(pay_id),

    base_salary DOUBLE PRECISION,
    regular_gross_paid DOUBLE PRECISION,
    ot_hours DOUBLE PRECISION,
    total_ot_paid DOUBLE PRECISION,
    total_other_pay DOUBLE PRECISION
);
