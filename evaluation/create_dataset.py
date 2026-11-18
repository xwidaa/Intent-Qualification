import csv
import random
from pathlib import Path

from src.data_loader import load_companies
from src.filters import filter_companies


QUERIES = [
    "Logistic companies in Romania",
    "Public software companies with more than 1,000 employees",
    "Clean energy startups founded after 2018 with fewer than 200 employees"
]

OUTPUT_PATH = Path("evaluation/labels.csv")
SAMPLES_PER_STATUS = 10
RANDOM_SEED = 42


def create_evaluation_dataset():
    random.seed(RANDOM_SEED)

    companies = load_companies()
    rows = []

    for query in QUERIES:
        results = filter_companies(companies, query)

        for status in ["MATCH", "UNKNOWN", "NO_MATCH"]:
            candidates = [
                (index, result)
                for index, result in enumerate(results)
                if result["status"] == status
            ]

            selected = random.sample(
                candidates,
                min(SAMPLES_PER_STATUS, len(candidates))
            )

            for index, result in selected:
                company = companies[index]

                rows.append({
                    "query": query,
                    "company_id": index,
                    "company_name": company.get("operational_name"),
                    "description": company.get("description", ""),
                    "primary_naics": (
                        company.get("primary_naics") or {}
                    ).get("label", ""),
                    "core_offerings": "; ".join(
                        str(value)
                        for value in company.get("core_offerings", [])
                    ),
                    "predicted_status": result["status"],
                    "ground_truth": "",
                    "notes": ""
                })

    OUTPUT_PATH.parent.mkdir(
        parents=True, exist_ok=True
    )

    with open(
        OUTPUT_PATH,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {len(rows)} evaluation examples.")
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    create_evaluation_dataset()
