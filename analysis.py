import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


DB_NAME = "jobs.db"
CHARTS_DIR = Path("charts")


def analyze_jobs():
    CHARTS_DIR.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM jobs", conn)
    conn.close()

    print(f"\n📊 Total Jobs: {len(df)}")

    # --------------------------------------------------
    # 1. Top Companies
    # --------------------------------------------------
    top_companies = df["company"].value_counts().head(10)

    print("\n🏢 Top 10 Companies by Job Count:")
    print(top_companies)

    top_companies.plot(kind="bar", figsize=(10, 5))
    plt.title("Top 10 Companies by Job Count")
    plt.xlabel("Company")
    plt.ylabel("Number of Jobs")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "top_companies.png", dpi=300)
    plt.close()

    # --------------------------------------------------
    # 2. Employment Type
    # --------------------------------------------------
    employment_types = df["employment_type"].value_counts()

    print("\n💼 Employment Type Distribution:")
    print(employment_types)

    employment_types.plot(kind="bar", figsize=(8, 5))
    plt.title("Employment Type Distribution")
    plt.xlabel("Employment Type")
    plt.ylabel("Number of Jobs")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "employment_type.png", dpi=300)
    plt.close()

    # --------------------------------------------------
    # 3. Seniority
    # --------------------------------------------------
    seniority = df["seniority"].value_counts().head(10)

    print("\n📈 Top Seniority Levels:")
    print(seniority)

    seniority.plot(kind="bar", figsize=(8, 5))
    plt.title("Job Listings by Seniority")
    plt.xlabel("Seniority")
    plt.ylabel("Number of Jobs")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "seniority.png", dpi=300)
    plt.close()

    # --------------------------------------------------
    # 4. Salary Analysis
    # --------------------------------------------------
    salary_df = df.dropna(
        subset=["min_salary", "max_salary"]
    ).copy()

    salary_df = salary_df[
        salary_df["salary_period"].fillna("").str.lower() == "annual"
    ].copy()

    if not salary_df.empty:

        salary_df["average_salary"] = (
            salary_df["min_salary"] +
            salary_df["max_salary"]
        ) / 2

        print("\n💰 Annual Salary Analysis by Currency:")

        for currency in salary_df["currency"].dropna().unique():

            currency_df = salary_df[
                salary_df["currency"] == currency
            ]

            print(f"\n{currency} Salary Statistics:")
            print(currency_df["average_salary"].describe())

            top_salary_jobs = (
                currency_df
                .sort_values(
                    "average_salary",
                    ascending=False
                )
                [
                    [
                        "title",
                        "company",
                        "average_salary",
                        "currency",
                        "salary_period"
                    ]
                ]
                .head(5)
            )

            print(f"\nTop 5 Highest-Paying {currency} Jobs:")
            print(top_salary_jobs.to_string(index=False))

    # --------------------------------------------------
    # 5. Job Categories
    # --------------------------------------------------
    categories = (
        df["categories"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
        .value_counts()
        .head(10)
    )

    print("\n🏷️ Top 10 Job Categories:")
    print(categories)

    categories.plot(kind="bar", figsize=(10, 5))
    plt.title("Top 10 Job Categories")
    plt.xlabel("Category")
    plt.ylabel("Number of Jobs")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "job_categories.png", dpi=300)
    plt.close()

    print("\n✅ Analysis completed successfully.")
    print(f"📁 Charts saved in: {CHARTS_DIR}/")


if __name__ == "__main__":
    analyze_jobs()