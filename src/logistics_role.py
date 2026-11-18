import re

from src.data_loader import load_companies


LOGISTICS_SERVICES = [
    r"\bfreight\s+(?:rail\s+)?transport(?:ation)?\b",
    r"\bfreight\s+forwarding\b",
    r"\bcargo\s+handling\b",
    r"\bcargo\s+transport(?:ation)?\b",
    r"\bwarehousing\b",
    r"\bthird[- ]party\s+logistics\b",
    r"\blogistics\s+services\b",
    r"\bport\s+operations\b",
    r"\bport\s+services\b",
    r"\bshipping\s+services\b",
    r"\brail\s+freight\b",
    r"\bmaritime\s+(?:and\s+river\s+)?port\s+services\b",
]


def evaluate_logistics_role(company):
    """
    Find explicit logistics-service evidence in
    the company's core offerings.

    MATCH means supporting evidence exists.
    UNKNOWN means evidence was not found.
    """

    offerings = company.get("core_offerings") or []

    if isinstance(offerings, str):
        offerings = [offerings]

    evidence = []

    for offering in offerings:
        text = str(offering).lower()

        for pattern in LOGISTICS_SERVICES:
            if re.search(pattern, text):
                evidence.append(offering)
                break

    return {
        "status": "MATCH" if evidence else "UNKNOWN",
        "evidence": evidence,
    }


LOGISTICS_NAICS_PATTERNS = [
    r"\bfreight\b",
    r"\btransportation\b",
    r"\bwarehousing\b",
    r"\bstorage\b",
    r"\bcargo\b",
    r"\bport\b",
    r"\bshipping\b",
    r"\bcourier\b",
    r"\bpostal\b",
    r"\blogistics\b",
]


def evaluate_primary_business(company):
    """
    Check whether the company's primary NAICS
    description indicates a logistics-related activity.
    """

    primary_naics = company.get("primary_naics") or {}

    if isinstance(primary_naics, dict):
        naics_text = " ".join(
            str(value)
            for value in primary_naics.values()
            if value is not None
        )
    else:
        naics_text = str(primary_naics)

    if not naics_text.strip():
        return {
            "status": "UNKNOWN",
            "naics": ""
        }

    matches = [
        pattern
        for pattern in LOGISTICS_NAICS_PATTERNS
        if re.search(pattern, naics_text, re.IGNORECASE)
    ]

    return {
        "status": "MATCH" if matches else "NO_MATCH",
        "naics": naics_text
    }


def evaluate_logistics_provider(company):
    service = evaluate_logistics_role(company)
    primary = evaluate_primary_business(company)

    if service["status"] == "MATCH" and primary["status"] == "MATCH":
        status = "STRONG_MATCH"

    elif service["status"] == "MATCH":
        status = "POSSIBLE_MATCH"

    else:
        status = "UNKNOWN"

    return {
        "status": status,
        "service_evidence": service["evidence"],
        "primary_naics": primary["naics"],
        "primary_status": primary["status"]
    }



def main():
    companies = load_companies()

    print("\n=== LOGISTICS PROVIDER QUALIFICATION ===")

    for company_id, company in enumerate(companies):
        result = evaluate_logistics_provider(company)

        if result["status"] == "UNKNOWN":
            continue

        print("\nCompany:", company.get("operational_name"))
        print("ID:", company_id)
        print("Status:", result["status"])
        print("Primary NAICS:", result["primary_naics"])
        print("Service evidence:", result["service_evidence"][:3])


if __name__ == "__main__":
    main()
