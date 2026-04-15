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

git clone, pip install -r requirements.txt, python manage.py
migrate, python manage.py seed_data, python manage.py runserver.

## Screenshot(s) of at least 3 pages (homepage, list view, analytics dashboard)


## manage.py check --deploy output



