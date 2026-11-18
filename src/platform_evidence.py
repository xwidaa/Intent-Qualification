import re

from collections import Counter
from src.data_loader import load_companies


PLATFORMS = [
    "shopify",
    "woocommerce",
    "bigcommerce",
    "magento",
    "adobe commerce"
]


def get_company_text(company):
    fields = [
        company.get("description"),
        company.get("business_model"),
        company.get("target_markets"),
        company.get("core_offerings")
    ]

    parts = []

    for field in fields:
        if isinstance(field, list):
            parts.extend(str(value) for value in field)
        elif field is not None:
            parts.append(str(field))

    return " ".join(parts)


def analyze_platform_mentions(companies):
    results = []
    counts = Counter()

    for company_id, company in enumerate(companies):
        text = get_company_text(company)

        for platform in PLATFORMS:
            pattern = re.escape(platform)

            if re.search(pattern, text, re.IGNORECASE):
                counts[platform] += 1

                results.append({
                    "company_id": company_id,
                    "company": (
                        company.get("operational_name")
                        or company.get("website")
                        or f"Company {company_id}"
                    ),
                    "platform": platform,
                    "text": text
                })

    return results, counts


def main():
    companies = load_companies()

    results, counts = analyze_platform_mentions(companies)

    print("\n=== PLATFORM MENTION ANALYSIS ===")

    print("Total companies:", len(companies))
    print("Platform mentions:", len(results))

    for platform in PLATFORMS:
        print(f"{platform}: {counts[platform]}")

    print("\n=== COMPANIES WITH PLATFORM MENTIONS ===")

    for result in results:
        print("\nCompany:", result["company"])
        print("Platform:", result["platform"])
        print("Description:", result["text"][:350])


if __name__ == "__main__":
    main()
