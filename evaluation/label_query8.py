import csv
from pathlib import Path

FILE_PATH = Path("evaluation/manual_review.csv")

LABELS = {
    172: ("UNCERTAIN", "Renewable energy company; startup status not confirmed"),
    213: ("UNCERTAIN", "Floating wind and solar technologies; startup status not confirmed"),
    304: ("NOT_RELEVANT", "Primarily sustainability and environmental consulting"),
    315: ("NOT_RELEVANT", "European public-private project rather than an independent startup"),
    291: ("UNCERTAIN", "Energy efficiency and monitoring; clean energy startup status unclear"),
    294: ("NOT_RELEVANT", "Primarily ESG and climate advisory services"),
    206: ("UNCERTAIN", "Renewable energy activities; startup status not confirmed"),
    327: ("UNCERTAIN", "Hydroelectric engineering; startup status not confirmed"),
    311: ("UNCERTAIN", "Solar and renewable energy engineering; startup status not confirmed"),
    185: ("UNCERTAIN", "Wind turbine technology; startup status not confirmed"),
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
        if int(row["query_id"]) != 8:
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

    print(f"Updated {updated} labels for Query 8.")


if __name__ == "__main__":
    main()
