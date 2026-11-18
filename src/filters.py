import re

from src.data_loader import load_companies
from src.query_parser import parse_query



INDUSTRY_KEYWORDS = {
    "software": [
        "software publishers",
        "software development",
        "software products",
        "software solutions",
        "custom computer programming"
    ],
    "logistics": [
        "freight forwarding",
        "freight transportation",
        "warehousing services",
        "third-party logistics",
        "logistics services"
    ],
    "pharmaceutical": [
        "pharmaceutical manufacturing",
        "pharmaceutical preparation",
        "drug manufacturing"
    ],
    "construction": [
        "construction of buildings",
        "construction contractor",
        "residential construction",
        "commercial construction"
    ],
    "fintech": [
        "financial technology",
        "payment processing",
        "digital banking",
        "financial transactions processing"
    ],
    "food_beverage": [
        "food manufacturing",
        "beverage manufacturing",
        "soft drink manufacturing"
    ],
    "clean_energy": [
        "renewable energy",
        "solar power",
        "wind energy",
        "wind turbine",
        "clean energy"
    ]
}


def check_numeric(value, threshold, operator):
    """Evaluate a numeric constraint."""

    if value is None:
        return "UNKNOWN"

    try:
        value = float(value)
    except (TypeError, ValueError):
        return "UNKNOWN"

    if operator == "greater":
        return "MATCH" if value > threshold else "NO_MATCH"

    return "MATCH" if value < threshold else "NO_MATCH"


def check_industry(company, industry):
    """Check industry using selected business activity signals."""

    keywords = INDUSTRY_KEYWORDS.get(industry)

    if not keywords:
        return "UNKNOWN"

    naics = company.get("primary_naics") or {}
    label = str(naics.get("label", "")).lower()

    offerings = company.get("core_offerings") or []

    activities = " ".join(
        str(item) for item in offerings
    ).lower()

    text = label + " " + activities

    if any(keyword in text for keyword in keywords):
        return "MATCH"


    if label or activities:
        return "NO_MATCH"

    return "UNKNOWN"


def check_company(company, constraints):
    """Evaluate all recognized structured constraints."""

    checks = {}

    if constraints["industry"] is not None:
        checks["industry"] = check_industry(
            company, constraints["industry"]
        )

    if constraints["country"] is not None:
        address = company.get("address") or {}
        country = address.get("country_code")

        if not country:
            checks["country"] = "UNKNOWN"
        elif str(country).lower() == constraints["country"]:
            checks["country"] = "MATCH"
        else:
            checks["country"] = "NO_MATCH"

    if constraints["is_public"] is not None:
        value = company.get("is_public")

        if not isinstance(value, bool):
            checks["is_public"] = "UNKNOWN"
        else:
            checks["is_public"] = (
                "MATCH"
                if value == constraints["is_public"]
                else "NO_MATCH"
            )

    if constraints["min_employees"] is not None:
        checks["min_employees"] = check_numeric(
            company.get("employee_count"),
            constraints["min_employees"],
            "greater"
        )

    if constraints["max_employees"] is not None:
        checks["max_employees"] = check_numeric(
            company.get("employee_count"),
            constraints["max_employees"],
            "less"
        )

    if constraints["min_revenue"] is not None:
        checks["min_revenue"] = check_numeric(
            company.get("revenue"),
            constraints["min_revenue"],
            "greater"
        )

    if constraints["founded_after"] is not None:
        checks["founded_after"] = check_numeric(
            company.get("year_founded"),
            constraints["founded_after"],
            "greater"
        )

    if not checks:
        status = "UNKNOWN"
    elif "NO_MATCH" in checks.values():
        status = "NO_MATCH"
    elif "UNKNOWN" in checks.values():
        status = "UNKNOWN"
    else:
        status = "MATCH"

    return {
        "company": company.get("operational_name"),
        "website": company.get("website"),
        "status": status,
        "checks": checks
    }


def filter_companies(companies, query):
    """Apply structured constraints to the dataset."""

    constraints = parse_query(query)

    results = [
        check_company(company, constraints)
        for company in companies
    ]

    return results


if __name__ == "__main__":

    companies = load_companies()

    queries = [
        "Logistic companies in Romania",
        "Public software companies with more than 1,000 employees",
        "Clean energy startups founded after 2018 with fewer than 200 employees"
    ]

    for query in queries:
        results = filter_companies(companies, query)

        matches = [
            item for item in results
            if item["status"] == "MATCH"
        ]

        unknown = [
            item for item in results
            if item["status"] == "UNKNOWN"
        ]

        rejected = [
            item for item in results
            if item["status"] == "NO_MATCH"
        ]

        print("\n" + "=" * 65)
        print("QUERY:", query)
        print("=" * 65)

        print(f"Total companies: {len(results)}")
        print(f"Matches: {len(matches)}")
        print(f"Unknown: {len(unknown)}")
        print(f"Rejected: {len(rejected)}")

        print("\nTOP MATCHES:")

        for item in matches[:10]:
            print(
                f"- {item['company']} "
                f"| {item['checks']}"
            )

        print("\nSAMPLE UNKNOWN:")

        for item in unknown[:3]:
            print(
                f"- {item['company']} "
                f"| {item['checks']}"
            )
