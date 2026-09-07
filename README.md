# Job Listings Scraper & Analysis

A Python-based data pipeline that collects current remote job listings from the Himalayas public Jobs API, stores structured data in CSV and SQLite, and performs analysis using Pandas and SQL with Matplotlib visualizations.

## Project Overview

This project demonstrates an end-to-end data workflow:

**API → Data Collection → Cleaning → CSV → SQLite → SQL/Pandas Analysis → Visualization**

The pipeline collects job information such as company, employment type, seniority, location, categories, salary details, posting date, and application links.

## Features

* Collects up to 500 job listings using API pagination
* Handles cursor-based pagination
* Removes duplicate job listings using unique job IDs
* Converts Unix timestamps into readable dates
* Stores structured data in CSV format
* Stores job listings in a SQLite database
* Uses SQL and Pandas for exploratory analysis
* Analyzes:

  * Top companies by number of listings
  * Employment type distribution
  * Seniority distribution
  * Salary statistics by currency
  * Highest-paying annual roles by currency
  * Most common job categories
* Generates high-resolution Matplotlib charts automatically

## Technologies Used

* Python
* Requests
* Pandas
* BeautifulSoup
* SQLite
* SQL
* Matplotlib
* Himalayas Jobs API

## Project Structure

```text
Job-Listing-Scrapper-using-python-main/
│
├── scraper.py
├── database.py
├── analysis.py
├── jobs.csv
├── jobs.db
├── requirements.txt
├── README.md
│
└── charts/
    ├── top_companies.png
    ├── employment_type.png
    ├── seniority.png
    └── job_categories.png
```

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Collect job listings

```bash
python scraper.py
```

This fetches up to 500 job listings and saves them to:

```text
jobs.csv
```

### 3. Create the SQLite database

```bash
python database.py
```

This stores the collected listings in:

```text
jobs.db
```

### 4. Run the analysis

```bash
python analysis.py
```

The analysis results are printed in the terminal and the generated charts are saved in the `charts/` directory.

## Analysis Performed

### Top Companies

Identifies companies with the highest number of job listings in the collected dataset.

### Employment Type

Analyzes the distribution of:

* Full Time
* Contractor
* Part Time
* Intern
* Temporary
* Other

### Seniority

Examines job listings across different seniority levels such as:

* Entry-level
* Mid-level
* Senior
* Manager
* Director
* Executive

### Salary Analysis

Salary analysis focuses on annual salaries and keeps currencies separate to avoid invalid comparisons between USD, EUR, INR, CAD, and GBP.

### Job Categories

Identifies the most frequently occurring job categories across the collected listings.

## Data Source

Job listings are collected from the **Himalayas Remote Jobs API**.

The API is publicly available and the dataset is refreshed periodically rather than being a real-time feed.

[Himalayas Remote Jobs API Documentation](https://himalayas.app/docs/remote-jobs-api?utm_source=chatgpt.com)

## Data Attribution

This project uses job listing data provided by Himalayas. Please refer to the Himalayas API documentation for the applicable data usage and attribution requirements.

## Future Improvements

* Add automated scheduled data collection
* Expand the dataset with additional API pages
* Add more detailed location and category analysis
* Add interactive dashboards using Power BI or Streamlit
* Track changes in job listings over time
* Add automated data-quality checks

## Author

Satya Prakash
