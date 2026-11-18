import math

from src.data_loader import load_companies
from src.query_parser import parse_query



SCANDINAVIA = {"dk", "no", "se"}

EUROPE = {
    "al", "ad", "at", "be", "ba", "bg", "hr", "cy",
    "cz", "dk", "ee", "fi", "fr", "de", "gr", "hu",
    "is", "ie", "it", "lv", "li", "lt", "lu", "mt",
    "md", "mc", "me", "nl", "mk", "no", "pl",
    "pt", "ro", "sm", "rs", "sk", "si", "es",
    "se", "ch", "ua", "gb", "va"
}

REGION_COUNTRIES = {
    "europe": EUROPE,
    "scandinavia": SCANDINAVIA
}


def numeric_check(value, threshold, operator):
    if value is None or value == "":
        return "UNKNOWN"

    try:
        number = float(value)
    except (ValueError, TypeError):
        return "UNKNOWN"

    if not math.isfinite(number):
        return "UNKNOWN"

    if operator == "gt":
        return "MATCH" if number > threshold else "NO_MATCH"

    if operator == "lt":
        return "MATCH" if number < threshold else "NO_MATCH"

    raise ValueError(f"Unsupported operator: {operator}")


def evaluate_company(company, constraints):
    checks = {}

    address = company.get("address") or {}


    if constraints.get("country"):
        country = str(address.get("country_code") or "").lower()

        checks["country"] = (
            "UNKNOWN" if not country
            else "MATCH" if country == constraints["country"]
            else "NO_MATCH"
        )


    if constraints.get("region"):
        region = constraints["region"]
        country = str(address.get("country_code") or "").lower()
        allowed = REGION_COUNTRIES.get(region)

        if not country or allowed is None:
            checks["region"] = "UNKNOWN"
        elif country in allowed:
            checks["region"] = "MATCH"
        elif region == "europe" and country in {"ru", "tr", "ge", "az"}:

            checks["region"] = "UNKNOWN"
        else:
            checks["region"] = "NO_MATCH"


    if constraints.get("is_public") is not None:
        value = company.get("is_public")

        if isinstance(value, bool):
            checks["is_public"] = (
                "MATCH"
                if value == constraints["is_public"]
                else "NO_MATCH"
            )
        else:
            checks["is_public"] = "UNKNOWN"


    numeric_fields = [
        ("min_employees", "employee_count", "gt"),
        ("max_employees", "employee_count", "lt"),
        ("min_revenue", "revenue", "gt"),
        ("founded_after", "year_founded", "gt")
    ]

    for key, field, operator in numeric_fields:
        threshold = constraints.get(key)

        if threshold is not None:
            checks[key] = numeric_check(
                company.get(field), threshold, operator
            )


    required_models = constraints.get("business_model", [])

    if required_models:
        values = company.get("business_model") or []

        if isinstance(values, str):
            values = [values]

        known_models = {
            str(value).strip().lower() for value in values
        }

        for model in required_models:
            key = f"business_model_{model.lower()}"

            checks[key] = (
                "MATCH"
                if model.lower() in known_models
                else "UNKNOWN"
            )


    if constraints.get("industry"):
        checks["industry"] = "UNKNOWN"

    if constraints.get("product_category"):
        checks["product_category"] = "UNKNOWN"

    if constraints.get("required_roles"):
        checks["business_role"] = "UNKNOWN"

    for requirement in constraints.get("soft_constraints", []):
        checks[requirement] = "UNKNOWN"


    if "NO_MATCH" in checks.values():
        status = "NO_MATCH"
    elif "UNKNOWN" in checks.values():
        status = "UNKNOWN"
    elif checks:
        status = "MATCH"
    else:
        status = "UNKNOWN"

    return {
        "company": company.get("operational_name"),
        "status": status,
        "checks": checks
    }


def main():
    companies = load_companies()

    queries = [
        "Construction companies in the United States with revenue over $50 million",
        "B2B SaaS companies providing HR solutions in Europe",
        "Renewable energy equipment manufacturers in Scandinavia",
        "Companies that manufacture or supply critical components for electric vehicle battery production"
    ]

    for query in queries:
        constraints = parse_query(query)

        results = [
            evaluate_company(company, constraints)
            for company in companies
        ]

        print("\n" + "=" * 65)
        print("QUERY:", query)

        for status in ["MATCH", "UNKNOWN", "NO_MATCH"]:
            count = sum(
                result["status"] == status
                for result in results
            )

            print(f"{status}: {count}")

        print("\nEXAMPLE CANDIDATES:")

        candidates = [
            result for result in results
            if result["status"] != "NO_MATCH"
        ]

        for result in candidates[:5]:
            print(
                result["company"],
                "|", result["status"],
                "|", result["checks"]
            )


if __name__ == "__main__":
    main()
