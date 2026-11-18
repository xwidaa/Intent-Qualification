import re

from src.data_loader import load_companies


HR_SOFTWARE_PATTERNS = [
    r"\bhr\s+(?:management\s+)?software\b",
    r"\bhuman\s+resources\s+software\b",
    r"\bpayroll\s+(?:management\s+)?software\b",
    r"\brecruitment\s+(?:management\s+)?software\b",
    r"\bcloud[- ]based\s+hr\b",
    r"\btalent\s+management\s+software\b",
]


def evaluate_hr_saas(company):
    models = company.get("business_model") or []

    if isinstance(models, str):
        models = [models]

    normalized_models = {
        str(model).strip().lower()
        for model in models
    }

    has_b2b = (
        "business-to-business" in normalized_models
        or "b2b" in normalized_models
    )

    has_saas = (
        "software-as-a-service" in normalized_models
        or "saas" in normalized_models
    )

    offerings = company.get("core_offerings") or []

    if isinstance(offerings, str):
        offerings = [offerings]

    hr_evidence = [
        offering
        for offering in offerings
        if any(
            re.search(pattern, str(offering), re.IGNORECASE)
            for pattern in HR_SOFTWARE_PATTERNS
        )
    ]

    primary_naics = company.get("primary_naics") or {}

    if isinstance(primary_naics, dict):
        naics_code = str(primary_naics.get("code") or "")
        naics_label = str(primary_naics.get("label") or "")
    else:
        naics_code = ""
        naics_label = str(primary_naics)

    is_software_publisher = (
        naics_code == "513210"
        or "software publishers" in naics_label.lower()
    )

    if has_b2b and has_saas and hr_evidence:
        status = (
            "STRONG_MATCH"
            if is_software_publisher
            else "POSSIBLE_MATCH"
        )
    else:
        status = "UNKNOWN"

    return {
        "status": status,
        "has_b2b": has_b2b,
        "has_saas": has_saas,
        "is_software_publisher": is_software_publisher,
        "evidence": hr_evidence
    }


def main():
    companies = load_companies()

    print("\n=== HR SAAS QUALIFICATION ===")

    matches = []

    for company_id, company in enumerate(companies):
        result = evaluate_hr_saas(company)

        if result["status"] != "UNKNOWN":
            matches.append((company_id, company, result))

    print("Companies with HR SaaS evidence:", len(matches))

    for company_id, company, result in matches:
        print("\nID:", company_id)
        print("Company:", company.get("operational_name"))
        print("Status:", result["status"])
        print("B2B:", result["has_b2b"])
        print("SaaS:", result["has_saas"])
        print("Software publisher:", result["is_software_publisher"])
        print("Evidence:", result["evidence"][:2])


if __name__ == "__main__":
    main()
