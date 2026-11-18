import csv
from pathlib import Path

FILE_PATH = Path("evaluation/manual_review.csv")

LABELS = {
    223: ("UNCERTAIN", "Online grocery retail; platform unverified"),
    224: ("UNCERTAIN", "Online grocery ordering; platform unverified"),
    214: ("UNCERTAIN", "E-commerce operations; platform unverified"),
    252: ("UNCERTAIN", "D2C packaging e-commerce; platform unverified"),
    227: ("UNCERTAIN", "Online home goods retail; platform unverified"),
    54: ("NOT_RELEVANT", "Payment processing provider, not an e-commerce merchant"),
    1: ("UNCERTAIN", "Digital customer platforms; direct e-commerce and platform unclear"),
    395: ("UNCERTAIN", "Online beverage retail; platform unverified"),
    241: ("UNCERTAIN", "Online apparel retail; platform unverified"),
    237: ("UNCERTAIN", "Online candy and merchandise retail; platform unverified"),
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
        if int(row["query_id"]) != 10:
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

    print(f"Updated {updated} labels for Query 10.")


if __name__ == "__main__":
    main()
