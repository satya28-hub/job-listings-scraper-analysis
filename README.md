# Job Listings Scraper & Analysis

A Python-based data pipeline that collects remote job listings from the **Himalayas Public Jobs API**, stores structured data in CSV and SQLite, performs exploratory analysis using Pandas and SQL, and provides an interactive job-search dashboard using Streamlit.

## Project Overview

This project demonstrates an end-to-end data workflow:

**API → Data Collection → Cleaning → CSV → SQLite → SQL/Pandas Analysis → Visualization → Interactive Job Search**

The pipeline collects job information such as company, employment type, seniority, location, categories, salary details, posting date, and application links.

## Features

### 1. Data Collection & Processing
- Collects up to 500 job listings using API pagination.
- Handles cursor-based pagination.
- Removes duplicate job listings using unique job IDs.
- Converts Unix timestamps into readable dates.
- Cleans and structures collected job data.

### 2. Data Storage
- Stores structured job data in CSV format.
- Stores job listings in a SQLite database.

### 3. Exploratory Data Analysis
Uses SQL and Pandas to analyze:
- Top companies by number of listings.
- Employment type distribution.
- Seniority distribution.
- Salary statistics by currency.
- Highest-paying annual roles by currency.
- Most common job categories.

### 4. Data Visualization
- Generates high-resolution Matplotlib charts.
- Visualizes employment type, seniority, top companies, and job categories.

### 5. Interactive Job Search Dashboard
Built using Streamlit, the dashboard allows users to:
- Search jobs by keywords.
- Filter jobs by employment type.
- Filter by seniority level.
- Filter by location.
- Filter by salary currency and salary period.
- Set minimum and maximum salary limits.
- Sort listings by newest, oldest, company name, and salary.
- Navigate through results using pagination.
- Download matching job listings as CSV.

## Technologies Used

- Python
- Requests
- Pandas
- NumPy
- Streamlit
- SQLite
- SQL
- Matplotlib
- Himalayas Jobs API

## Project Structure

```text
job-listings-scraper-analysis/
│
├── app.py
├── scraper.py
├── database.py
├── analysis.py
├── jobs.csv
├── jobs.db
├── requirements.txt
├── README.md
├── job_scraper_project_notebook.ipynb
│
└── charts/
    ├── top_companies.png
    ├── employment_type.png
    ├── seniority.png
    └── job_categories.png
```

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/satya28-hub/job-listings-scraper-analysis.git
```

### 2. Navigate to the Project Directory

```bash
cd job-listings-scraper-analysis
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Collect Job Listings

```bash
python scraper.py
```

This fetches up to 500 job listings and saves the collected data to:

```text
jobs.csv
```

### 5. Create the SQLite Database

```bash
python database.py
```

This stores the collected job listings in:

```text
jobs.db
```

### 6. Run the Analysis

```bash
python analysis.py
```

The analysis results are printed in the terminal, and generated charts are saved in the `charts/` directory.

### 7. Launch the Interactive Dashboard

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal to access the Job Search & Job Analytics dashboard.

**Note:** The dashboard searches the locally stored dataset (`jobs.db` or `jobs.csv`). Running the dashboard does not automatically fetch new listings from the API. Run the scraper separately to refresh the dataset.

## Analysis Performed

### Top Companies

Identifies companies with the highest number of job listings in the collected dataset.

### Employment Type

Analyzes the distribution of:
- Full Time
- Contractor
- Part Time
- Intern
- Temporary
- Other

### Seniority

Examines job listings across different seniority levels, such as:
- Entry-level
- Mid-level
- Senior
- Manager
- Director
- Executive

### Salary Analysis

Analyzes salary information while keeping different currencies separate to avoid invalid comparisons between USD, EUR, INR, CAD, and GBP.

### Job Categories

Identifies the most frequently occurring job categories across the collected listings.

## Data Source

Job listings are collected from the **Himalayas Remote Jobs API**.

[Himalayas Remote Jobs API Documentation](https://himalayas.app/docs/remote-jobs-api)

The dataset is refreshed when the scraper is executed rather than functioning as a real-time feed.

## Data Attribution

This project uses job listing data provided by Himalayas. Please refer to the Himalayas API documentation for applicable data usage and attribution requirements.

## Future Improvements

- Add automated scheduled data collection.
- Expand the dataset with additional API pages.
- Add more detailed location and category analysis.
- Track changes in job listings over time.
- Implement automated data-quality checks.
- Enhance interactive dashboard visualizations.

## Author

**Satya Prakash**

GitHub: [satya28-hub](https://github.com/satya28-hub)