
import csv
from pathlib import Path


FILE_PATH = Path("evaluation/labels_enriched.csv")

LABELS = {
    5: ("NOT_RELEVANT", "Main activity is fuel retail, not logistics services."),
    10: ("RELEVANT", "Provides port operations and cargo handling services."),
    278: ("RELEVANT", "Public software engineering company with over 1000 employees."),
    268: ("UNCERTAIN", "Software-related services, but primarily outsourcing and customer experience."),
    275: ("NOT_RELEVANT", "Primarily a venture builder rather than a software provider."),
    199: ("RELEVANT", "Young, small company developing wind turbine equipment."),
    172: ("UNCERTAIN", "Renewable energy company, but startup independence is unclear."),
    303: ("UNCERTAIN", "Young renewable energy consultancy; core business interpretation is ambiguous."),
    267: ("RELEVANT", "Public IT and software services company with over 1000 employees."),
    282: ("RELEVANT", "Public software development company with over 1000 employees."),
    281: ("NOT_RELEVANT", "IT services provider, not a Romanian logistics company."),
    112: ("NOT_RELEVANT", "Software company, but not publicly traded."),
    206: ("UNCERTAIN", "Small recent company combining data centers and renewable energy."),
    185: ("RELEVANT", "Founded in 2019, 4 employees, develops wind turbines."),
    205: ("UNCERTAIN", "Renewable energy manufacturer with missing employee and founding data."),
    210: ("NOT_RELEVANT", "Founded in 1933 with 640 employees.")
}


def apply_labels():
    with open(FILE_PATH, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        fieldnames = reader.fieldnames

    updated = 0

    for row in rows:
        company_id = int(row["company_id"])

        if company_id not in LABELS:
            continue

        label, reason = LABELS[company_id]

        existing = row["ground_truth"].strip()

        if existing and existing != label:
            raise ValueError(
                f"Conflicting label for company ID {company_id}"
            )

        row["ground_truth"] = label
        row["notes"] = reason
        updated += 1

    with open(FILE_PATH, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated {updated} examples.")
    print(f"Saved to {FILE_PATH}")


if __name__ == "__main__":
    apply_labels()
