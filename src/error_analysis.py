from src.data_loader import load_companies
from src.filters import filter_companies


QUERIES = [
    "Logistic companies in Romania",
    "Public software companies with more than 1,000 employees",
    "Clean energy startups founded after 2018 with fewer than 200 employees"
]


def analyze_results(companies, query):
    results = filter_companies(companies, query)

    print("\n" + "=" * 70)
    print("QUERY:", query)
    print("=" * 70)

    selected = [
        result for result in results
        if result["status"] == "MATCH"
    ]

    print(f"\nSelected companies: {len(selected)}")

    for result in selected[:10]:
        company = next(
            (
                c for c in companies
                if c.get("website") == result["website"]
                and c.get("operational_name") == result["company"]
            ),
            None
        )

        if company is None:
            continue

        print("\nCompany:", result["company"])

        print(
            "Primary industry:",
            company.get("primary_naics", {}).get("label")
        )

        print(
            "Country:",
            company.get("address", {}).get("country_code")
        )

        print("Checks:", result["checks"])

        print(
            "Description:",
            str(company.get("description", ""))[:350]
        )

        print("-" * 70)


def main():
    companies = load_companies()

    for query in QUERIES:
        analyze_results(companies, query)


if __name__ == "__main__":
    main()
