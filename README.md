# CIS9440-Assignment-NYCPayroll
NYC Payroll Data Warehouse
Topic: Cloud-Based ELT Pipeline + BigQuery Star Schema
Cloud Platform: Google Cloud Platform (GCP)

			Project Overview

This project implements a complete ELT (Extract–Load–Transform) pipeline using:

	Google Cloud Storage (GCS) for raw data storage

	Cloud Run for containerized Python ELT

	BigQuery for data warehouse storage

	Star Schema dimensional model (Kimball methodology)

The source dataset is the NYC Payroll Data (2025) CSV file.

			Cloud Architecture

NYC Payroll CSV│Google Cloud Storage
	Cloud Run (ELT API) containerized Python
		BigQuery Data Warehouse
			- Staging_Payroll
			- Dim_Agency
			- Dim_Employee
			- Dim_Title
			- Dim_Date
			- Fact_Payroll


			Date Warehouse Schema (Star Schema)

Dimensions

	Dim_Agency - agency name, borough
	Dim_Employee - first name, middle initial, last name
	Dim_Title - title description, leave status
	Dim_Date - employee start date, payroll fiscal yeat date

Fact Table

	Surrogate key
	Foreign keys
	salary, hours, overtime, other pay

A star schema diagram - docs/star_schema_NYCPayroll.png


			ELT Pipeline Process

Extract

	Raw CSV uploaded to:
		gs://<your-bucket>/NYC_Payroll_2025.csv

Load

	Cloud Run Python script loads CSV → BigQuery:
		nyc_payroll_dw.staging_payroll

Transform

	The pipeline runs SQL files to build:
		- Dim_Agency
		- Dim_Employee
		- Dim_Title
		- Dim_Date
		- Fact_Payroll

	Facts join to dimensions using surrogate keys.

			Cloud Run ELT Script

Located in:
	elt/elt_bigquery.py

This handles:
	Reading CSV from GCS
	Loading staging table
	Running all SQL scripts
	Building dimensions and fact tables
	Returning JSON response

Dockerfile:
	Defines environment for Cloud Run:
		elt/Dockerfile

Dependencies - 

	Located in:
		elt/requirements.txt

	Includes:
		google-cloud-bigquery
		google-cloud-storage
		pandas
		pyarrow
		flask
		functions-framework

How to Deploy to Cloud Run - 
	Build the container
		gcloud builds submit --tag gcr.io/<project-id>/nyc-payroll-elt

Deploy to Cloud Run - 
	gcloud run deploy nyc-payroll-elt \
	    --image gcr.io/<project-id>/nyc-payroll-elt \
	    --platform managed \
	    --region us-central1 \
	    --allow-unauthenticated

Trigger the pipeline - 
	Send GET/POST request in browser:
		https://<cloud-run-url>

Validation - 
	staging table row count = 13,072
	fact table row count = 13,072
	dimension tables populated
	date dimension fully populated
	surrogate keys implemented
	BigQuery SQL executed successfully

			References

- Google Cloud Run Documentation
- Google BigQuery Documentation
- NYC Open Payroll Date 