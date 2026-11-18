import re

from src.data_loader import load_companies


FINTECH_PATTERNS = [
    r"\bdigital payment",
    r"\bonline payment",
    r"\bpayment gateway",
    r"\bpayment processing",
    r"\bdigital wallet",
    r"\bmobile banking",
    r"\bdigital banking",
    r"\bonline banking",
    r"\bbanking platform",
    r"\bblockchain.based financial",
    r"\bdecentralized lending",
    r"\bonline credit",
    r"\bonline loan",
    r"\bonline money transfer platform",
    r"\bfinancial technology",
]

BANKING_ALTERNATIVE_PATTERNS = [
    r"\bdigital wallet",
    r"\bmobile banking",
    r"\bdigital banking",
    r"\bbusiness banking",
    r"\bpayment gateway",
    r"\bdigital payment",
    r"\bonline payment",
    r"\bdecentralized lending",
    r"\bonline credit",
    r"\bonline loan",
    r"\bmulti.bank account",
    r"\bonline money transfer platform",
]

FINANCIAL_NAICS_PATTERNS = [
    r"\bfinancial\b",
    r"\bcredit\b",
    r"\bbanking\b",
    r"\bmonetary\b",
    r"\btransactions processing\b",
]


def find_evidence(offerings, patterns):
    evidence = []

    for offering in offerings:
        text = str(offering).lower()

        if any(
            re.search(pattern, text)
            for pattern in patterns
        ):
            evidence.append(str(offering))

    return evidence


def evaluate_fintech(company):
    offerings = company.get("core_offerings") or []

    if isinstance(offerings, str):
        offerings = [offerings]

    primary_naics = company.get("primary_naics") or {}

    if isinstance(primary_naics, dict):
        naics_text = str(
            primary_naics.get("label") or ""
        )
    else:
        naics_text = str(primary_naics)

    financial_industry = any(
        re.search(pattern, naics_text, re.IGNORECASE)
        for pattern in FINANCIAL_NAICS_PATTERNS
    )

    fintech_evidence = find_evidence(
        offerings, FINTECH_PATTERNS
    )

    banking_evidence = find_evidence(
        offerings, BANKING_ALTERNATIVE_PATTERNS
    )

    if financial_industry and fintech_evidence and banking_evidence:
        status = "STRONG_MATCH"

    elif fintech_evidence:
        status = "POSSIBLE_MATCH"

    else:
        status = "UNKNOWN"

    return {
        "status": status,
        "financial_industry": financial_industry,
        "fintech_evidence": fintech_evidence,
        "banking_evidence": banking_evidence,
        "growth_status": "UNVERIFIED"
    }


def main():
    companies = load_companies()

    print("\n=== FINTECH QUALIFICATION ===")

    counts = {
        "STRONG_MATCH": 0,
        "POSSIBLE_MATCH": 0,
        "UNKNOWN": 0
    }

    for company_id, company in enumerate(companies):
        result = evaluate_fintech(company)

        counts[result["status"]] += 1

        if result["status"] == "UNKNOWN":
            continue

        print("\nID:", company_id)
        print("Company:", company.get("operational_name"))
        print("Status:", result["status"])
        print(
            "Financial industry:",
            result["financial_industry"]
        )
        print(
            "Fintech evidence:",
            result["fintech_evidence"][:3]
        )
        print(
            "Banking evidence:",
            result["banking_evidence"][:3]
        )
        print("Growth:", result["growth_status"])

    print("\nSUMMARY")
    print(counts)


if __name__ == "__main__":
    main()
