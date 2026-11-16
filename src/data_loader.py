
import ast
import json
from pathlib import Path


DATA_PATH = Path("data/companies.jsonl")


def parse_dictionary(value):
    """Convert dictionary-like strings into dictionaries."""

    if isinstance(value, dict):
        return value

    if isinstance(value, str):
        try:
            result = ast.literal_eval(value)
            if isinstance(result, dict):
                return result
        except (ValueError, SyntaxError):
            pass

    return {}


def normalize_company(company):
    """Normalize a company profile while preserving its data."""

    company = company.copy()

    company["address"] = parse_dictionary(
        company.get("address")
    )

    company["primary_naics"] = parse_dictionary(
        company.get("primary_naics")
    )

    secondary = company.get("secondary_naics")

    if secondary is None:
        company["secondary_naics"] = []
    elif isinstance(secondary, list):
        company["secondary_naics"] = [
            parse_dictionary(item) for item in secondary
        ]
    else:
        company["secondary_naics"] = [
            parse_dictionary(secondary)
        ]

    for field in [
        "business_model",
        "target_markets",
        "core_offerings"
    ]:
        if not isinstance(company.get(field), list):
            company[field] = []

    return company


def load_companies(path=DATA_PATH):
    """Load and normalize all companies from JSONL."""

    companies = []

    with open(path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                company = json.loads(line)
                companies.append(normalize_company(company))
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON at line {line_number}"
                ) from error

    return companies


if __name__ == "__main__":
    companies = load_companies()

    print(f"Loaded {len(companies)} companies.")

    print("\nFirst company:")
    print(companies[0]["operational_name"])

    print("\nNormalized address:")
    print(companies[0]["address"])

    print("\nNormalized NAICS:")
    print(companies[0]["primary_naics"])

    print("\nSecondary NAICS:")
    print(companies[0]["secondary_naics"])
