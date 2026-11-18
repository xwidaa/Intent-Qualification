import csv
from pathlib import Path

FILE_PATH = Path("evaluation/manual_review.csv")

LABELS = {
    28: ("RELEVANT", "US construction company; revenue above $50M"),
    43: ("RELEVANT", "US general contractor; revenue above $50M"),
    32: ("RELEVANT", "US commercial construction; revenue above $50M"),
    38: ("RELEVANT", "US construction and design-build; revenue above $50M"),
    37: ("RELEVANT", "US infrastructure construction; revenue above $50M"),
    36: ("RELEVANT", "US engineering and construction; revenue above $50M"),
    26: ("RELEVANT", "US engineering and construction; revenue above $50M"),
    29: ("RELEVANT", "US homebuilding company; revenue above $50M"),
    24: ("RELEVANT", "US transportation infrastructure construction; revenue above $50M"),
    34: ("RELEVANT", "Construction operations in the US; revenue above $50M"),
}


def main():
    with open(FILE_PATH, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        rows = list(reader)

    updated = 0

    for row in rows:
        if int(row["query_id"]) != 5:
            continue

        company_id = int(row["company_id"])

        if company_id in LABELS:
            label, notes = LABELS[company_id]
            row["manual_label"] = label
            row["review_notes"] = notes
            updated += 1

    with open(FILE_PATH, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated {updated} labels for Query 5.")


if __name__ == "__main__":
    main()
