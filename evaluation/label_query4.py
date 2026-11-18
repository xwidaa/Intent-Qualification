import csv
from pathlib import Path

FILE_PATH = Path("evaluation/manual_review.csv")

LABELS = {
    257: ("RELEVANT", "Custom cosmetic packaging manufacturing"),
    264: ("RELEVANT", "Cosmetic containers and packaging supply"),
    258: ("RELEVANT", "Cosmetic bottles and packaging manufacturing"),
    262: ("RELEVANT", "Customized cosmetic packaging supplier"),
    266: ("RELEVANT", "Cosmetic packaging manufacturing and export"),
    259: ("RELEVANT", "OEM and ODM cosmetic packaging manufacturing"),
    255: ("RELEVANT", "Skincare bottles and cosmetic packaging"),
    260: ("RELEVANT", "Cosmetic packaging production and distribution"),
    263: ("RELEVANT", "Cosmetic packaging manufacturing and wholesale"),
    250: ("RELEVANT", "Cosmetic bottles and jars supplier"),
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
        if int(row["query_id"]) != 4:
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

    print(f"Updated {updated} labels for Query 4.")


if __name__ == "__main__":
    main()
