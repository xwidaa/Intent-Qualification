import csv
from pathlib import Path


INPUT_FILE = Path("results/results.csv")
OUTPUT_FILE = Path("evaluation/manual_review.csv")


def main():
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        results = list(csv.DictReader(file))

    review_rows = []

    for result in results:
        review_rows.append({
            "query_id": result["query_id"],
            "query": result["query"],
            "rank": result["rank"],
            "company_id": result["company_id"],
            "company_name": result["company_name"],
            "qualification_status": result[
                "qualification_status"
            ],
            "evidence": result["evidence"],
            "constraint_checks": result[
                "constraint_checks"
            ],
            "manual_label": "",
            "review_notes": ""
        })

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=review_rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(review_rows)

    print(
        f"Created {OUTPUT_FILE} "
        f"with {len(review_rows)} rows."
    )


if __name__ == "__main__":
    main()
