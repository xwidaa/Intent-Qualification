INTENT_PROFILES = {
    "logistics": (
        "A company whose primary business is providing "
        "freight transportation, cargo handling, "
        "warehousing, shipping or third-party logistics "
        "services to other businesses."
    ),

    "software": (
        "A company whose main business is developing, "
        "engineering, publishing or selling software "
        "products and software development services."
    ),

    "clean_energy": (
        "A company whose main business is developing, "
        "manufacturing, generating or supplying renewable "
        "energy technologies and clean energy solutions."
    ),

    "pharmaceutical": (
        "A company whose primary business is developing "
        "or manufacturing pharmaceutical drugs and "
        "medical treatments."
    ),

    "construction": (
        "A company providing building construction, "
        "civil engineering construction or general "
        "contracting services."
    ),

    "fintech": (
        "A company developing financial technology "
        "products such as digital banking, payments, "
        "financial infrastructure or lending platforms."
    ),

    "food_beverage": (
        "A company manufacturing food or beverage "
        "products for commercial distribution."
    )
}


def get_semantic_query(query, constraints):
    industry = constraints.get("industry")

    if industry in INTENT_PROFILES:
        return INTENT_PROFILES[industry]

    return query
