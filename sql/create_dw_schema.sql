-- =====================================================
-- NYC Payroll Data Warehouse Schema
-- =====================================================

CREATE SCHEMA IF NOT EXISTS nyc_payroll_dw;

-- ====================
-- Dimension Tables
-- ====================

CREATE TABLE nyc_payroll_dw.dim_agency (
    agency_id SERIAL PRIMARY KEY,
    agency_name VARCHAR(255) UNIQUE
);

CREATE TABLE nyc_payroll_dw.dim_title (
    title_id SERIAL PRIMARY KEY,
    title_description VARCHAR(255)
);

CREATE TABLE nyc_payroll_dw.dim_location (
    location_id SERIAL PRIMARY KEY,
    work_location_borough VARCHAR(100)
);

CREATE TABLE nyc_payroll_dw.dim_employee (
    employee_id SERIAL PRIMARY KEY,
    agency_start_date DATE
);

CREATE TABLE nyc_payroll_dw.dim_time (
    time_id SERIAL PRIMARY KEY,
    fiscal_year INT
);

-- ====================
-- Fact Table
-- ====================

CREATE TABLE nyc_payroll_dw.fact_payroll (
    fact_id SERIAL PRIMARY KEY,
    employee_id INT REFERENCES nyc_payroll_dw.dim_employee(employee_id),
    agency_id INT REFERENCES nyc_payroll_dw.dim_agency(agency_id),
    title_id INT REFERENCES nyc_payroll_dw.dim_title(title_id),
    location_id INT REFERENCES nyc_payroll_dw.dim_location(location_id),
    time_id INT REFERENCES nyc_payroll_dw.dim_time(time_id),
    pay_basis VARCHAR(50),
    base_salary NUMERIC(12,2),
    regular_hours NUMERIC(8,2),
    regular_gross_paid NUMERIC(12,2),
    ot_hours NUMERIC(8,2),
    total_ot_paid NUMERIC(12,2),
    total_other_pay NUMERIC(12,2)
);
