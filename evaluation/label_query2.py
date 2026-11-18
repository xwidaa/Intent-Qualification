import csv
from pathlib import Path

FILE_PATH = Path("evaluation/manual_review.csv")

LABELS = {
    269: ("UNCERTAIN", "Software services; public status of Canadian subsidiary needs verification"),
    285: ("RELEVANT", "Enterprise software development and IT services"),
    274: ("RELEVANT", "Software and ICT solutions; publicly traded"),
    278: ("RELEVANT", "Software engineering and platform development"),
    282: ("RELEVANT", "Software product and application development"),
    273: ("UNCERTAIN", "Primarily BPO and consulting; software activity requires review"),
    283: ("RELEVANT", "Enterprise IT and software solutions"),
    280: ("RELEVANT", "Custom software development and technology consulting"),
    277: ("RELEVANT", "Application development and IT services"),
    284: ("RELEVANT", "Software development and digital engineering"),
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
        if int(row["query_id"]) != 2:
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
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated {updated} labels for Query 2.")


if __name__ == "__main__":
    main()
