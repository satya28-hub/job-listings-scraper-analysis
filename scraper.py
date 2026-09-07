
import requests
import pandas as pd
import time

API_URL = "https://himalayas.app/jobs/api"
MAX_JOBS = 500


def scrape_jobs():
    all_jobs = []
    cursor = None

    while len(all_jobs) < MAX_JOBS:
        params = {"limit": 20}

        if cursor:
            params["cursor"] = cursor

        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        jobs = data.get("jobs", [])

        if not jobs:
            break

        for job in jobs:

            locations = job.get("locationRestrictions", [])

            location = ", ".join(

                loc if isinstance(loc, str) else loc.get("name", "")
                for loc in locations
       )

            categories = job.get("categories", [])

            all_jobs.append({
                "title": job.get("title"),
                "company": job.get("companyName"),
                "employment_type": job.get("employmentType"),
                "seniority": ", ".join(job.get("seniority", [])),
                "location": location,
                "categories": ", ".join(categories),
                "min_salary": job.get("minSalary"),
                "max_salary": job.get("maxSalary"),
                "salary_period": job.get("salaryPeriod"),
                "currency": job.get("currency"),
                "date_posted": job.get("pubDate"),
                "application_link": job.get("applicationLink"),
                "job_id": job.get("guid")
            })

            if len(all_jobs) >= MAX_JOBS:
                break

        cursor = data.get("nextCursor")

        if not cursor:
            break

        time.sleep(0.5)

    df = pd.DataFrame(all_jobs)

    # Remove duplicate job listings
    df = df.drop_duplicates(subset="job_id")

    # Convert posting date to readable format
    df["date_posted"] = pd.to_datetime(
        df["date_posted"],
        unit="s",
        errors="coerce"
    )

    df.to_csv("jobs.csv", index=False)

    print(f"✅ Scraped {len(df)} jobs and saved to jobs.csv")


if __name__ == "__main__":
    scrape_jobs()