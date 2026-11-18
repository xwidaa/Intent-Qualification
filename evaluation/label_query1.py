import csv
from pathlib import Path

FILE_PATH = Path("evaluation/manual_review.csv")

LABELS = {
    20: ("RELEVANT", "Logistics facilities and warehousing"),
    6: ("RELEVANT", "Railway infrastructure and freight support"),
    10: ("RELEVANT", "Port operations and cargo handling"),
    11: ("NOT_RELEVANT", "Agricultural commodity processing"),
    13: ("NOT_RELEVANT", "Wholesale and retail distribution"),
    8: ("NOT_RELEVANT", "Automotive manufacturing"),
    21: ("NOT_RELEVANT", "Intralogistics equipment supplier"),
    23: ("NOT_RELEVANT", "Beverage manufacturing"),
    7: ("NOT_RELEVANT", "Truck and bus sales and maintenance"),
    1: ("NOT_RELEVANT", "Consumer goods distribution"),
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
        if int(row["query_id"]) != 1:
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

    print(f"Updated {updated} labels for Query 1.")


if __name__ == "__main__":
    main()
