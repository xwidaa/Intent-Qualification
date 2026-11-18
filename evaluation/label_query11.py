import csv
from pathlib import Path

FILE_PATH = Path("evaluation/manual_review.csv")

LABELS = {
    208: ("RELEVANT", "Wind turbine design and manufacturing in Denmark"),
    401: ("UNCERTAIN", "Wind turbine facility; manufacturing role unclear"),
    178: ("RELEVANT", "Small wind turbine manufacturing in Sweden"),
    172: ("RELEVANT", "Wind turbine manufacturing in Norway"),
    170: ("RELEVANT", "Wind turbines and energy storage equipment"),
    181: ("RELEVANT", "Wind turbine manufacturing in Denmark"),
    211: ("RELEVANT", "Small wind turbine design and production"),
    198: ("RELEVANT", "Solar panels, inverters and renewable energy equipment"),
    190: ("RELEVANT", "Solar panels and energy storage equipment manufacturing"),
    186: ("RELEVANT", "Wind and solar system component manufacturing"),
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
        if int(row["query_id"]) != 11:
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

    print(f"Updated {updated} labels for Query 11.")


if __name__ == "__main__":
    main()
