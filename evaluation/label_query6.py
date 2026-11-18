import csv
from pathlib import Path

FILE_PATH = Path("evaluation/manual_review.csv")

LABELS = {
    449: ("RELEVANT", "Pharmaceutical research, manufacturing and distribution"),
    470: ("RELEVANT", "Drug development and pharmaceutical manufacturing"),
    476: ("RELEVANT", "Pharmaceutical manufacturing and distribution"),
    456: ("RELEVANT", "Biopharmaceutical research and development"),
    475: ("RELEVANT", "Pharmaceutical CDMO and API manufacturing"),
    474: ("RELEVANT", "Pharmaceutical development and contract manufacturing"),
    453: ("RELEVANT", "Prescription medicines and pharmaceutical production"),
    471: ("RELEVANT", "Pharmaceutical products and API manufacturing"),
    465: ("RELEVANT", "Pharmaceutical products and supplement manufacturing"),
    447: ("RELEVANT", "Biopharmaceutical research and manufacturing"),
}


def main():
    with open(
        FILE_PATH, "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        rows = list(reader)

    updated = 0

    for row in rows:
        if int(row["query_id"]) != 6:
            continue

        company_id = int(row["company_id"])

        if company_id in LABELS:
            label, notes = LABELS[company_id]
            row["manual_label"] = label
            row["review_notes"] = notes
            updated += 1

    with open(
        FILE_PATH, "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=fieldnames
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated {updated} labels for Query 6.")


if __name__ == "__main__":
    main()
