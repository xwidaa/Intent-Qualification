from src.data_loader import load_companies
from src.filters import INDUSTRY_KEYWORDS


WEIGHTS = {
    "naics": 0.50,
    "offerings": 0.35,
    "description": 0.15
}


def keyword_score(text, keywords):
    """Measure how many industry signals appear in text."""

    if not text or not keywords:
        return 0.0

    text = str(text).lower()

    matches = sum(
        1 for keyword in keywords
        if keyword in text
    )

    return matches / len(keywords)


def calculate_industry_score(company, industry):
    """Calculate a weighted industry relevance score."""

    keywords = INDUSTRY_KEYWORDS.get(industry, [])

    if not keywords:
        return 0.0

    naics = company.get("primary_naics") or {}
    naics_text = naics.get("label", "")

    offerings = " ".join(
        str(item)
        for item in company.get("core_offerings", [])
    )

    description = company.get("description", "")

    naics_score = keyword_score(naics_text, keywords)
    offerings_score = keyword_score(offerings, keywords)
    description_score = keyword_score(description, keywords)

    final_score = (
        WEIGHTS["naics"] * naics_score
        + WEIGHTS["offerings"] * offerings_score
        + WEIGHTS["description"] * description_score
    )

    return round(final_score, 4)


if __name__ == "__main__":
    companies = load_companies()

    industries = [
        "logistics",
        "software",
        "clean_energy"
    ]

    for industry in industries:
        ranked = []

        for company in companies:
            score = calculate_industry_score(
                company, industry
            )

            ranked.append({
                "name": company.get("operational_name"),
                "score": score
            })

        ranked.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        print("\n" + "=" * 60)
        print("INDUSTRY:", industry)
        print("=" * 60)

        for item in ranked[:10]:
            print(
                f"{str(item['name']):35} "
                f"Score: {item['score']:.4f}"
            )
