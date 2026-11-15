"""Interactive job search interface for the scraped Himalayas job listings."""

from pathlib import Path
import sqlite3

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "jobs.db"
CSV_PATH = BASE_DIR / "jobs.csv"

st.set_page_config(page_title="Job Search & Analytics", page_icon="💼", layout="wide")


@st.cache_data(show_spinner=False)
def load_jobs():
    """Load jobs from SQLite, falling back to the CSV export."""
    if DB_PATH.exists():
        try:
            with sqlite3.connect(DB_PATH) as conn:
                jobs = pd.read_sql_query("SELECT * FROM jobs", conn)
            if not jobs.empty:
                return jobs
        except (sqlite3.Error, pd.errors.DatabaseError):
            pass

    if CSV_PATH.exists():
        return pd.read_csv(CSV_PATH)

    return pd.DataFrame()


def clean_text_column(series):
    return series.fillna("").astype(str).str.strip()


def search_jobs(
    jobs,
    keyword="",
    employment_types=None,
    seniority_levels=None,
    locations=None,
    currency="All",
    salary_period="All",
    minimum_salary=None,
    maximum_salary=None,
):
    """Return jobs matching the selected search terms and filters."""
    results = jobs.copy()

    # Search across the fields available in this project's dataset.
    searchable_columns = [
        column
        for column in ["title", "company", "location", "categories", "seniority", "employment_type"]
        if column in results.columns
    ]
    if keyword.strip() and searchable_columns:
        search_text = results[searchable_columns].fillna("").astype(str).agg(" ".join, axis=1)
        results = results[search_text.str.contains(keyword.strip(), case=False, regex=False)]

    if employment_types:
        results = results[results["employment_type"].isin(employment_types)]
    if seniority_levels:
        # Seniority may contain multiple comma-separated values in one record.
        seniority_text = clean_text_column(results["seniority"])
        seniority_mask = pd.Series(False, index=results.index)
        for level in seniority_levels:
            seniority_mask |= seniority_text.str.contains(level, case=False, regex=False)
        results = results[seniority_mask]
    if locations:
        location_text = clean_text_column(results["location"])
        location_mask = pd.Series(False, index=results.index)
        for location in locations:
            location_mask |= location_text.str.contains(location, case=False, regex=False)
        results = results[location_mask]

    if currency != "All" and "currency" in results.columns:
        results = results[results["currency"].fillna("").str.upper() == currency]
    if salary_period != "All" and "salary_period" in results.columns:
        results = results[results["salary_period"].fillna("").str.lower() == salary_period.lower()]

    if minimum_salary is not None or maximum_salary is not None:
        min_values = pd.to_numeric(results["min_salary"], errors="coerce")
        max_values = pd.to_numeric(results["max_salary"], errors="coerce")
        salary_mask = min_values.notna() & max_values.notna()
        # Keep a salary range if it overlaps the user's requested range.
        if minimum_salary is not None:
            salary_mask &= max_values >= minimum_salary
        if maximum_salary is not None:
            salary_mask &= min_values <= maximum_salary
        results = results[salary_mask]

    return results


jobs = load_jobs()
st.title("💼 Job Search & Job Analytics")
st.caption("Search and filter the job listings collected by this project's Himalayas API scraper.")

if jobs.empty:
    st.error("No job data found. Run `python scraper.py` and `python database.py`, or place jobs.csv beside app.py.")
    st.stop()

# Normalize fields that may be absent in older exports and prepare display columns.
for column in [
    "title", "company", "employment_type", "seniority", "location", "categories",
    "salary_period", "currency", "application_link", "date_posted",
]:
    if column not in jobs.columns:
        jobs[column] = ""

for column in ["min_salary", "max_salary"]:
    if column not in jobs.columns:
        jobs[column] = pd.NA
    jobs[column] = pd.to_numeric(jobs[column], errors="coerce")

jobs["date_posted"] = pd.to_datetime(jobs["date_posted"], errors="coerce", utc=True)

st.sidebar.header("Find a job")
keyword = st.sidebar.text_input(
    "Search keywords",
    placeholder="e.g. data analyst, Python, marketing",
    help="Searches job title, company, location, categories, seniority and employment type.",
)

employment_options = sorted(value for value in jobs["employment_type"].dropna().astype(str).unique() if value.strip())
seniority_options = sorted({
    part.strip()
    for value in jobs["seniority"].dropna().astype(str)
    for part in value.split(",")
    if part.strip()
})
location_options = sorted({
    part.strip()
    for value in jobs["location"].dropna().astype(str)
    for part in value.split(",")
    if part.strip()
})
currency_options = sorted(value.upper() for value in jobs["currency"].dropna().astype(str).unique() if value.strip())
period_options = sorted(value.lower() for value in jobs["salary_period"].dropna().astype(str).unique() if value.strip())

selected_employment = st.sidebar.multiselect("Employment type", employment_options)
selected_seniority = st.sidebar.multiselect("Seniority", seniority_options)
selected_locations = st.sidebar.multiselect("Location", location_options)
selected_currency = st.sidebar.selectbox("Salary currency", ["All"] + currency_options)
selected_period = st.sidebar.selectbox("Salary period", ["All"] + period_options)

st.sidebar.caption("Salary filters use the selected currency and salary period. Listings without salary details are excluded when a salary limit is entered.")
min_salary_input = st.sidebar.number_input("Minimum salary", min_value=0.0, value=0.0, step=5000.0)
max_salary_input = st.sidebar.number_input("Maximum salary (0 = no limit)", min_value=0.0, value=0.0, step=5000.0)
minimum_salary = min_salary_input if min_salary_input > 0 else None
maximum_salary = max_salary_input if max_salary_input > 0 else None

if minimum_salary is not None and maximum_salary is not None and minimum_salary > maximum_salary:
    st.sidebar.error("Minimum salary cannot be greater than maximum salary.")
    st.stop()

filtered = search_jobs(
    jobs,
    keyword=keyword,
    employment_types=selected_employment,
    seniority_levels=selected_seniority,
    locations=selected_locations,
    currency=selected_currency,
    salary_period=selected_period,
    minimum_salary=minimum_salary,
    maximum_salary=maximum_salary,
)

sort_by = st.selectbox(
    "Sort results",
    ["Newest first", "Oldest first", "Company A–Z", "Salary: high to low"],
    horizontal=True,
)
if sort_by == "Newest first":
    filtered = filtered.sort_values("date_posted", ascending=False, na_position="last")
elif sort_by == "Oldest first":
    filtered = filtered.sort_values("date_posted", ascending=True, na_position="last")
elif sort_by == "Company A–Z":
    filtered = filtered.sort_values("company", key=lambda col: col.fillna("").str.lower())
else:
    filtered = filtered.assign(_salary_sort=filtered["max_salary"].fillna(filtered["min_salary"]))
    filtered = filtered.sort_values("_salary_sort", ascending=False, na_position="last").drop(columns="_salary_sort")

metric1, metric2, metric3 = st.columns(3)
metric1.metric("Jobs in dataset", f"{len(jobs):,}")
metric2.metric("Matching jobs", f"{len(filtered):,}")
metric3.metric("Companies", f"{filtered['company'].nunique():,}")
st.divider()

if filtered.empty:
    st.info("No jobs match these search criteria. Try removing a filter or using broader keywords.")
else:
    page_size = st.selectbox("Results per page", [10, 20, 50], index=1)
    total_pages = max(1, (len(filtered) + page_size - 1) // page_size)
    page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)
    start = (int(page) - 1) * page_size
    page_results = filtered.iloc[start : start + page_size]
    st.caption(f"Showing {start + 1}–{start + len(page_results)} of {len(filtered)} matching jobs")

    for _, job in page_results.iterrows():
        title = str(job.get("title") or "Untitled role")
        company = str(job.get("company") or "Company not listed")
        st.subheader(title)
        st.write(f"**{company}** · {job.get('location') or 'Location not specified'}")

        details = []
        for field in ["employment_type", "seniority"]:
            value = job.get(field)
            if pd.notna(value) and str(value).strip():
                details.append(str(value))
        if pd.notna(job.get("date_posted")):
            details.append(f"Posted: {job['date_posted'].strftime('%d %b %Y')}")
        if pd.notna(job.get("min_salary")) or pd.notna(job.get("max_salary")):
            low = "Not listed" if pd.isna(job.get("min_salary")) else f"{job['min_salary']:,.0f}"
            high = "Not listed" if pd.isna(job.get("max_salary")) else f"{job['max_salary']:,.0f}"
            currency = str(job.get("currency") or "")
            period = str(job.get("salary_period") or "")
            details.append(f"Salary: {low}–{high} {currency} ({period})")
        if details:
            st.caption(" | ".join(details))
        categories = str(job.get("categories") or "").replace(",", " · ")
        if categories:
            st.caption(f"Categories: {categories}")
        link = str(job.get("application_link") or "").strip()
        if link.startswith(("https://", "http://")):
            st.markdown(f"[View job and apply]({link})")
        st.divider()

    export_columns = [
        column for column in [
            "title", "company", "employment_type", "seniority", "location", "categories",
            "min_salary", "max_salary", "salary_period", "currency", "date_posted", "application_link",
        ] if column in filtered.columns
    ]
    csv_data = filtered[export_columns].to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download matching jobs as CSV",
        data=csv_data,
        file_name="filtered_jobs.csv",
        mime="text/csv",
    )

with st.expander("About this dataset"):
    st.write(
        "These results come from the job records collected by scraper.py from the Himalayas Jobs API. "
        "The search operates on the locally saved CSV or SQLite database; it does not make a live API request for every search."
    )
