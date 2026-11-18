import csv
from pathlib import Path

from src.data_loader import load_companies


INPUT_PATH = Path("evaluation/labels.csv")
OUTPUT_PATH = Path("evaluation/labels_enriched.csv")


def enrich_labels():
    companies = load_companies()

    with open(INPUT_PATH, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        fieldnames = list(reader.fieldnames)

    extra_fields = [
        "country_code",
        "employee_count",
        "year_founded",
        "is_public",
        "revenue"
    ]

    for field in extra_fields:
        if field not in fieldnames:
            fieldnames.append(field)

    for row in rows:
        company_id = int(row["company_id"])
        company = companies[company_id]

        address = company.get("address") or {}

        row["country_code"] = address.get("country_code", "")
        row["employee_count"] = company.get("employee_count")
        row["year_founded"] = company.get("year_founded")
        row["is_public"] = company.get("is_public")
        row["revenue"] = company.get("revenue")

    with open(
        OUTPUT_PATH, "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Enriched {len(rows)} examples.")
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    enrich_labels()
