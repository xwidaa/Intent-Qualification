import csv
from pathlib import Path

FILE_PATH = Path("evaluation/manual_review.csv")

LABELS = {
    66: ("RELEVANT", "B2B SaaS HRM and payroll software"),
    89: ("RELEVANT", "Subscription-based HR software for businesses"),
    85: ("RELEVANT", "Cloud-based HR management software"),
    108: ("RELEVANT", "B2B SaaS talent and HR management"),
    77: ("RELEVANT", "Cloud HRM platform for businesses"),
    110: ("RELEVANT", "HRMS and payroll SaaS solutions"),
    65: ("RELEVANT", "B2B SaaS recruitment and HR platform"),
    64: ("RELEVANT", "Cloud HR and recruitment software"),
    95: ("RELEVANT", "Cloud-based HR and payroll system"),
    88: ("RELEVANT", "SaaS talent management and HR software"),
}


def main():
    with open(
        FILE_PATH,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        rows = list(reader)

    updated = 0

    for row in rows:
        if int(row["query_id"]) != 7:
            continue

        company_id = int(row["company_id"])

        if company_id in LABELS:
            label, notes = LABELS[company_id]
            row["manual_label"] = label
            row["review_notes"] = notes
            updated += 1

    with open(
        FILE_PATH,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated {updated} labels for Query 7.")


if __name__ == "__main__":
    main()
