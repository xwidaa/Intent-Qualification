import re


INDUSTRIES = {
    "software": ["software"],
    "logistics": ["logistics", "logistic"],
    "pharmaceutical": ["pharmaceutical", "pharma"],
    "construction": ["construction"],
    "fintech": ["fintech"],
    "food_beverage": ["food and beverage"],
    "clean_energy": ["clean energy", "renewable energy"],
    "ecommerce": ["e-commerce", "ecommerce"],
    "packaging": ["packaging materials", "packaging"],
    "ev_battery": [
        "electric vehicle battery",
        "ev battery",
        "battery production"
    ]
}

COUNTRIES = {
    "romania": "ro",
    "germany": "de",
    "france": "fr",
    "switzerland": "ch",
    "united states": "us"
}

REGIONS = {
    "europe": "europe",
    "scandinavia": "scandinavia"
}



def detect_keywords(text, mapping):
    for category, keywords in mapping.items():

        if isinstance(keywords, str):
            keywords = [keywords]

        if any(keyword in text for keyword in keywords):
            return category

    return None



def parse_query(query):
    text = query.lower()

    constraints = {
        "industry": detect_keywords(text, INDUSTRIES),
        "country": next(
    (
        code for name, code in COUNTRIES.items()
        if re.search(r"\b" + re.escape(name) + r"\b", text)
    ),
    None
),
        "region": next(
    (
        region for name, region in REGIONS.items()
        if re.search(r"\b" + re.escape(name) + r"\b", text)
    ),
    None
),
        "is_public": None,
        "min_employees": None,
        "max_employees": None,
        "min_revenue": None,
        "founded_after": None,
        "business_model": [],
        "required_roles": [],
        "product_category": None,
        "soft_constraints": []
    }




    if re.search(r"\bpublic(?:ly traded)?\b", text):
        constraints["is_public"] = True


    employee_min = re.search(
        r"(?:more than|over)\s+([\d,]+)\s+employees",
        text
    )

    if employee_min:
        constraints["min_employees"] = int(
            employee_min.group(1).replace(",", "")
        )

    employee_max = re.search(
        r"(?:fewer than|less than|under)\s+([\d,]+)\s+employees",
        text
    )

    if employee_max:
        constraints["max_employees"] = int(
            employee_max.group(1).replace(",", "")
        )


    founded = re.search(r"founded after\s+(\d{4})", text)

    if founded:
        constraints["founded_after"] = int(founded.group(1))


    revenue_match = re.search(
        r"revenue\s+(?:over|above|more than)\s+"
        r"\$?\s*([\d,.]+)\s*(million|billion|m|b)?",
        text
    )

    if revenue_match:
        amount = float(
            revenue_match.group(1).replace(",", "")
        )

        unit = revenue_match.group(2)

        multipliers = {
            "million": 1_000_000,
            "m": 1_000_000,
            "billion": 1_000_000_000,
            "b": 1_000_000_000
        }

        constraints["min_revenue"] = (
            amount * multipliers.get(unit, 1)
        )

    if re.search(r"\bb2b\b", text):
        constraints["business_model"].append("B2B")

    if re.search(r"\bsaas\b", text):
        constraints["business_model"].append("SaaS")



    if "manufactur" in text:
        constraints["required_roles"].append("manufacturer")

    if re.search(r"\bsupply\b|\bsupplying\b|\bsupplier\b", text):
        constraints["required_roles"].append("supplier")

    if "providing" in text:
        constraints["required_roles"].append("provider")

    if "competing with" in text:
        constraints["required_roles"].append("competitor")

    if "using" in text:
        constraints["required_roles"].append("platform_user")


    if "packaging" in text and "cosmetic" in text:
        constraints["product_category"] = "cosmetic_packaging"

    elif "hr solutions" in text:
        constraints["product_category"] = "hr_software"

    elif "battery" in text and "component" in text:
        constraints["product_category"] = "ev_battery_components"

    elif "renewable energy equipment" in text:
        constraints["product_category"] = "renewable_energy_equipment"


    if "startup" in text:
        constraints["soft_constraints"].append("startup")

    if "fast-growing" in text:
        constraints["soft_constraints"].append("fast_growing")

    if "critical" in text:
        constraints["soft_constraints"].append("critical_components")

    return constraints


if __name__ == "__main__":
    queries = [
        "Construction companies in the United States with revenue over $50 million",
        "B2B SaaS companies providing HR solutions in Europe",
        "Companies that manufacture or supply critical components for electric vehicle battery production"
    ]

    for query in queries:
        print("\nQUERY:", query)
        print("PARSED:", parse_query(query))
