import csv
from pathlib import Path

FILE_PATH = Path("evaluation/manual_review.csv")

LABELS = {
    336: ("RELEVANT", "Cathode, anode and electrolyte manufacturing for EV batteries"),
    338: ("RELEVANT", "Battery electrode materials and battery management systems"),
    368: ("RELEVANT", "LFP cathode materials for automotive batteries"),
    365: ("RELEVANT", "Cathode materials, electrolytes and battery precursors"),
    332: ("RELEVANT", "Solid-state battery electrolyte manufacturing"),
    362: ("RELEVANT", "Lithium-ion and lithium-metal battery separators"),
    345: ("RELEVANT", "LFP, LMFP and anode material manufacturing"),
    367: ("RELEVANT", "LFP and LMFP battery cathode materials"),
    343: ("RELEVANT", "Cathode, anode and electrolyte materials"),
    364: ("RELEVANT", "Battery materials and specialized production equipment"),
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
        if int(row["query_id"]) != 12:
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

    print(f"Updated {updated} labels for Query 12.")


if __name__ == "__main__":
    main()
