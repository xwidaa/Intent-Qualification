import numpy as np
from sentence_transformers import SentenceTransformer
from src.deduplication import deduplicate_results
from src.intent_profiles import get_semantic_query
from src.data_loader import load_companies
from src.query_parser import parse_query
from src.semantic_ranker import company_to_text, MODEL_NAME


def numeric_check(value, threshold, operator):
    if value is None:
        return "UNKNOWN"

    try:
        value = float(value)
    except (ValueError, TypeError):
        return "UNKNOWN"

    if np.isnan(value):
        return "UNKNOWN"

    if operator == "gt":
        return "MATCH" if value > threshold else "NO_MATCH"

    return "MATCH" if value < threshold else "NO_MATCH"


def check_hard_constraints(company, constraints):
    checks = {}

    if constraints["country"] is not None:
        country = (company.get("address") or {}).get("country_code")

        if not country:
            checks["country"] = "UNKNOWN"
        else:
            checks["country"] = (
                "MATCH"
                if str(country).lower() == constraints["country"]
                else "NO_MATCH"
            )

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

    numeric_fields = [
        ("min_employees", "employee_count", "gt"),
        ("max_employees", "employee_count", "lt"),
        ("min_revenue", "revenue", "gt"),
        ("founded_after", "year_founded", "gt")
    ]

    for constraint, field, operator in numeric_fields:
        threshold = constraints.get(constraint)

        if threshold is not None:
            checks[constraint] = numeric_check(
                company.get(field),
                threshold,
                operator
            )

    if "NO_MATCH" in checks.values():
        status = "NO_MATCH"
    elif "UNKNOWN" in checks.values():
        status = "UNKNOWN"
    else:
        status = "MATCH"

    return status, checks


def hybrid_rank(query, companies, model, embeddings, top_k=10):
    constraints = parse_query(query)

    semantic_query = get_semantic_query(
    query, constraints
)

    query_embedding = model.encode(
        [semantic_query],
        normalize_embeddings=True
    )[0]

    scores = embeddings @ query_embedding

    candidates = []

    for index, company in enumerate(companies):
        status, checks = check_hard_constraints(
            company, constraints
        )

        if status == "NO_MATCH":
            continue

        candidates.append({
            "company_id": index,
            "name": company.get("operational_name"),
            "semantic_score": float(scores[index]),
            "hard_status": status,
            "checks": checks
        })

    candidates.sort(
        key=lambda item: (
            item["hard_status"] == "MATCH",
            item["semantic_score"]
        ),
        reverse=True
    )

    unique_candidates = deduplicate_results(
    candidates, companies
)

    return unique_candidates[:top_k]


def main():
    companies = load_companies()

    print("Loading model...")
    model = SentenceTransformer(MODEL_NAME)

    texts = [company_to_text(c) for c in companies]

    print("Generating embeddings...")
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        batch_size=32,
        show_progress_bar=True
    )

    queries = [
        "Logistic companies in Romania",
        "Public software companies with more than 1,000 employees",
        "Clean energy startups founded after 2018 with fewer than 200 employees",
        "Companies supplying packaging materials for cosmetics brands"
    ]

    for query in queries:
        print("\n" + "=" * 70)
        print("QUERY:", query)
        print("=" * 70)

        results = hybrid_rank(
            query, companies, model, embeddings
        )

        if not results:
            print("No candidates found.")
            continue

        for item in results:
            print(
                f"{str(item['name'])[:32]:32} "
                f"Score: {item['semantic_score']:.4f} "
                f"Hard: {item['hard_status']}"
            )


if __name__ == "__main__":
    main()
