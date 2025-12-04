			NYC Payroll Data Warehouse – Data Dictionary

This document describes all tables in the nyc_payroll_dw dataset, including dimensions and fact tables.

Table: staging_payroll (Raw Load Layer)

		Column Name	Type	Description
		Agency Name	STRING	Full name of the NYC agency
		Agency Start Date	STRING	Employee agency start date (MM/DD/YYYY)
		Fiscal Year	INT64	Fiscal year of payroll
		First Name	STRING	Employee first name
		Last Name	STRING	Employee last name
		Mid Init	STRING	Middle initial
		Work Location Borough	STRING	Borough where employee works
		Title Description	STRING	Employee’s position title
		Leave Status as of June 30	STRING	Active, LOA, etc.
		Base Salary	FLOAT64	Annual base salary
		Regular Hours	FLOAT64	Total regular hours
		Regular Gross Paid	FLOAT64	Gross salary for the period
		OT Hours	FLOAT64	Overtime hours
		Total OT Paid	FLOAT64	Total overtime pay
		Total Other Pay	FLOAT64	Additional pay

Table: dim_agency

		Column	Type	Description
		agency_id (PK)	INT64	Surrogate key
		agency_name	STRING	Name of agency
		work_location_borough	STRING	Borough of work location

Table: dim_employee

		Column	Type	Description
		employee_id (PK)	INT64	Surrogate key
		first_name	STRING	Employee first name
		last_name	STRING	Employee last name
		middle_initial	STRING	Middle initial

Table: dim_title

		Column	Type	Description
		title_id (PK)	INT64	Surrogate key
		title_description	STRING	Employee job title
		leave_status	STRING	Leave status

Table: dim_date (Role-Playing)

		Column	Type	Description
		date_id (PK)	INT64	Surrogate key
		full_date	DATE	Calendar date
		year	INT64	Year
		quarter	INT64	Quarter
		month	INT64	Month number
		month_name	STRING	Month name
		day	INT64	Day of month
		day_of_week	INT64	Day of week index
		day_name	STRING	Name of day
		week_number	INT64	Week of year

	Role-played as:
		Payroll Date
		Employee Start Date

Table: fact_payroll

		Column	Type	Description
		payroll_fact_id (PK)	STRING (UUID)	Surrogate key
		agency_id (FK)	INT64	References dim_agency
		employee_id (FK)	INT64	References dim_employee
		title_id (FK)	INT64	References dim_title
		payroll_date_id (FK)	INT64	References dim_date (Fiscal Year End: June 30)
		start_date_id (FK)	INT64	References dim_date (Agency Start Date)
		base_salary	FLOAT64	Base annual salary
		regular_hours	FLOAT64	Total regular hours
		regular_gross_paid	FLOAT64	Regular gross pay
		ot_hours	FLOAT64	Overtime hours
		total_ot_paid	FLOAT64	Total overtime pay
		total_other_pay	FLOAT64	Additional pay