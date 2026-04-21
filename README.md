# cis4930-sp26-project-group-13-project-2
# Django Project 3

## Group Members

* William Kilduff - FSUID: WRK24 - Github: Killiam-duff
* Ty Officer - FSUID: TRO23 - Github: officety01
* Jack Waite - FSUID: JRW24a - Github: SirCatolot

## Project Description

This project is a full-stack Django web application that integrates two prior projects into a single website.

Project 1 (MLB Batting Analysis): We analyzed MLB batting statistics using Python, NumPy, and pandas to identify trends in player performance, including batting average, home runs, WAR, OPS, and other offensive metrics.
Project 2 (Weather API Pipeline): We built an automated data pipeline using the Open-Meteo API to collect weather data for multiple Florida panhandle cities (Tallahassee, Pensacola, and Navarre), storing structured data for future analysis.

The goal is to demonstrate full-stack data engineering, combining data analysis, APIs, and web development into one system.

## Link to original data set

Original Data set source: https://github.com/Killiam-duff/cis4930-sp26-project-group-13.git

## API Source

API source: https://open-meteo.com/en/docs

## Application Features

Django ORM with relational database design (3+ models)
ForeignKey relationships between datasets
Model field choices (CSV vs API source tracking)
Custom seed script for CSV ingestion (project 1 data)
API ingestion via Django management command (project 2 data)

## Setup instructions (sample for now)

git clone https://github.com/Killiam-duff/cis4930-sp26-django-project-group-13.git 

pip install -r requirements.txt

python manage.py migrate

python manage.py seed_data

python manage.py fetch_data  

python manage.py runserver
## Screenshot(s) of at least 3 pages (homepage, list view, analytics dashboard)


## manage.py check --deploy output

WARNINGS:
?: (security.W004) You have not set a value for the SECURE_HSTS_SECONDS setting. If your entire site is served only over SSL, you may want to consider setting a value and enabling HTTP Strict Transport Security. Be sure to read the documentation first; enabling HSTS carelessly can cause serious, irreversible problems.
?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True. Unless your site should be available over both SSL and non-SSL connections, you may want to either set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.
?: (security.W009) Your SECRET_KEY has less than 50 characters, less than 5 unique characters, or it's prefixed with 'django-insecure-' indicating that it was generated automatically by Django. Please generate a long and random value, otherwise many of Django's security-critical features will be vulnerable to attack.
?: (security.W012) SESSION_COOKIE_SECURE is not set to True. Using a secure-only session cookie makes it more difficult for network traffic sniffers to hijack user sessions.
?: (security.W016) You have 'django.middleware.csrf.CsrfViewMiddleware' in your MIDDLEWARE, but you have not set CSRF_COOKIE_SECURE to True. Using a secure-only CSRF cookie makes it more difficult for network traffic sniffers to steal the CSRF token.

System check identified 5 issues (0 silenced).
