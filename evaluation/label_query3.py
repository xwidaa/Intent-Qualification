import csv
from pathlib import Path

FILE_PATH = Path("evaluation/manual_review.csv")

LABELS = {
    388: ("RELEVANT", "Artisanal soft drink manufacturing"),
    385: ("RELEVANT", "Wine production"),
    393: ("RELEVANT", "Soft drinks and beer manufacturing"),
    389: ("RELEVANT", "Regional beverage manufacturing"),
    386: ("RELEVANT", "Food and beverage manufacturing"),
    381: ("RELEVANT", "Prepared food and beverage production"),
    380: ("RELEVANT", "Wine-based alcoholic beverage manufacturing"),
    387: ("RELEVANT", "Wine and spirits production"),
    399: ("RELEVANT", "Wine production and bottling"),
    398: ("RELEVANT", "Artisanal kombucha manufacturing"),
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
        if int(row["query_id"]) != 3:
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

    print(f"Updated {updated} labels for Query 3.")


if __name__ == "__main__":
    main()
