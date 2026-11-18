import csv
from pathlib import Path

FILE_PATH = Path("evaluation/manual_review.csv")

LABELS = {
    62: ("UNCERTAIN", "Digital payments and wallet; fast growth unverified"),
    54: ("UNCERTAIN", "Payment technology; fast growth unverified"),
    53: ("UNCERTAIN", "Blockchain-based lending; fast growth unverified"),
    57: ("UNCERTAIN", "Digital business banking; fast growth unverified"),
    55: ("UNCERTAIN", "Multi-bank digital platform; fast growth unverified"),
    51: ("UNCERTAIN", "Online money transfers; fintech role and growth unclear"),
    46: ("UNCERTAIN", "Digital wallet and electronic payments; growth unverified"),
    50: ("NOT_RELEVANT", "Primarily cash management and cash transport"),
    59: ("NOT_RELEVANT", "Traditional private debt and equity financing"),
    61: ("NOT_RELEVANT", "Traditional commodity trade financing"),
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
        if int(row["query_id"]) != 9:
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

    print(f"Updated {updated} labels for Query 9.")


if __name__ == "__main__":
    main()
