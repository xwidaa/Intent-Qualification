import re

from src.data_loader import load_companies
from src.query_parser import parse_query


PRODUCT_PATTERNS = {
    "cosmetic_packaging": [
        r"cosmetic.*packag",
        r"packag.*cosmetic",
        r"cosmetic.*bottle",
        r"cosmetic.*container",
        r"beauty.*packag",
        r"skincare.*packag",
    ],
    "renewable_energy_equipment": [
        r"wind turbine",
        r"solar panel",
        r"solar module",
        r"tidal turbine",
        r"renewable energy equipment",
        r"biomass boiler",
    ],
    "ev_battery_components": [
        r"battery.*cathode",
        r"cathode.*material",
        r"battery.*anode",
        r"anode.*material",
        r"battery.*electrolyte",
        r"solid electrolyte",
        r"battery.*separator",
        r"lithium iron phosphate",
        r"battery.*raw material",
    ],
}


ROLE_PATTERNS = {
    "manufacturer": [
        r"manufactur",
        r"produc",
        r"fabricat",
    ],
    "supplier": [
        r"supply",
        r"suppli",
        r"wholesale",
        r"distribution",
        r"sales",
    ],
}


def contains_pattern(text, patterns):
    return any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in patterns
    )


def evaluate_business_role(company, constraints):
    """
    Look for explicit evidence linking a requested
    product to a manufacturing or supplying activity.

    MATCH means positive evidence was found.
    UNKNOWN means the available rules cannot decide.
    """

    product_category = constraints.get("product_category")
    required_roles = constraints.get("required_roles", [])

    if product_category not in PRODUCT_PATTERNS:
        return {
            "status": "UNKNOWN",
            "evidence": [],
            "reason": "Product category not supported by this verifier"
        }

    offerings = company.get("core_offerings") or []

    product_patterns = PRODUCT_PATTERNS[product_category]
    evidence = []

    for offering in offerings:
        text = str(offering).lower()

        product_match = contains_pattern(
            text, product_patterns
        )

        if not product_match:
            continue

        for role in required_roles:
            patterns = ROLE_PATTERNS.get(role, [])

            if contains_pattern(text, patterns):
                evidence.append({
                    "offering": offering,
                    "role": role
                })

    if evidence:
        return {
            "status": "MATCH",
            "evidence": evidence,
            "reason": "Product and business role supported by core offerings"
        }

    return {
        "status": "UNKNOWN",
        "evidence": [],
        "reason": "Insufficient explicit product-role evidence"
    }


def main():
    companies = load_companies()

    queries = [
        "Companies that could supply packaging materials for a direct-to-consumer cosmetics brand",
        "Renewable energy equipment manufacturers in Scandinavia",
        "Companies that manufacture or supply critical components for electric vehicle battery production"
    ]

    for query in queries:
        constraints = parse_query(query)

        matches = []

        for company_id, company in enumerate(companies):
            result = evaluate_business_role(
                company, constraints
            )

            if result["status"] == "MATCH":
                matches.append((company_id, company, result))

        print("\n" + "=" * 65)
        print("QUERY:", query)
        print(f"Companies with explicit evidence: {len(matches)}")

        for company_id, company, result in matches[:10]:
            print(
                f"\n{company.get('operational_name')} "
                f"(ID: {company_id})"
            )

            for evidence in result["evidence"][:2]:
                print(
                    f"  Role: {evidence['role']} "
                    f"| Offering: {evidence['offering']}"
                )


if __name__ == "__main__":
    main()
