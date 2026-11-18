import csv
import sys

from src.data_loader import load_companies


def main():
    query_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    companies = load_companies()

    with open(
        "results/results.csv",
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        results = list(csv.DictReader(file))

    selected = [
        row for row in results
        if int(row["query_id"]) == query_id
    ]

    if not selected:
        print(f"No results found for Query {query_id}")
        return

    print("\nQUERY:", selected[0]["query"])

    for row in selected:
        company_id = int(row["company_id"])
        company = companies[company_id]

        print("\n" + "=" * 65)
        print("RANK:", row["rank"])
        print("ID:", company_id)
        print("COMPANY:", row["company_name"])
        print("COUNTRY/ADDRESS:", company.get("address"))
        print("PRIMARY NAICS:", company.get("primary_naics"))
        print("BUSINESS MODEL:", company.get("business_model"))
        print("CORE OFFERINGS:")

        for offering in company.get("core_offerings") or []:
            print(" -", offering)

        print("DESCRIPTION:", company.get("description"))


if __name__ == "__main__":
    main()
