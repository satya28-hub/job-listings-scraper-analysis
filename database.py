import sqlite3
import pandas as pd


DB_NAME = "jobs.db"
CSV_FILE = "jobs.csv"


def create_database():
    df = pd.read_csv(CSV_FILE)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            employment_type TEXT,
            seniority TEXT,
            location TEXT,
            categories TEXT,
            min_salary REAL,
            max_salary REAL,
            salary_period TEXT,
            currency TEXT,
            date_posted TEXT,
            application_link TEXT
        )
    """)

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT OR REPLACE INTO jobs (
                job_id,
                title,
                company,
                employment_type,
                seniority,
                location,
                categories,
                min_salary,
                max_salary,
                salary_period,
                currency,
                date_posted,
                application_link
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["job_id"],
            row["title"],
            row["company"],
            row["employment_type"],
            row["seniority"],
            row["location"],
            row["categories"],
            row["min_salary"],
            row["max_salary"],
            row["salary_period"],
            row["currency"],
            row["date_posted"],
            row["application_link"]
        ))

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM jobs")
    job_count = cursor.fetchone()[0]

    conn.close()

    print(f"✅ Database updated successfully")
    print(f"📊 Total jobs in database: {job_count}")


if __name__ == "__main__":
    create_database()
