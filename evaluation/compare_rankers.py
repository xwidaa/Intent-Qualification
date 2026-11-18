import csv
from pathlib import Path

from sentence_transformers import SentenceTransformer

from src.data_loader import load_companies
from src.query_parser import parse_query
from src.semantic_ranker import company_to_text, MODEL_NAME
from src.intent_profiles import get_semantic_query
from src.hybrid_ranker import hybrid_rank


LABELS_PATH = Path("evaluation/labels_enriched.csv")


def load_labels():
    with open(
        LABELS_PATH,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        return [
            row for row in csv.DictReader(file)
            if row["ground_truth"]
        ]


def rank_all(query, companies, model, embeddings, expanded=False):
    constraints = parse_query(query)

    semantic_query = (
        get_semantic_query(query, constraints)
        if expanded else query
    )

    from src.hybrid_ranker import check_hard_constraints

    query_embedding = model.encode(
        [semantic_query],
        normalize_embeddings=True
    )[0]

    scores = embeddings @ query_embedding

    results = []

    for index, company in enumerate(companies):
        status, _ = check_hard_constraints(
            company, constraints
        )

        if status == "NO_MATCH":
            continue

        results.append((index, status, float(scores[index])))

    results.sort(
        key=lambda x: (x[1] == "MATCH", x[2]),
        reverse=True
    )

    return {
        company_id: position
        for position, (company_id, _, _) in enumerate(
            results, start=1
        )
    }


def main():
    companies = load_companies()
    labels = load_labels()

    print("Loading model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Generating embeddings...")
    embeddings = model.encode(
        [company_to_text(c) for c in companies],
        normalize_embeddings=True,
        batch_size=32,
        show_progress_bar=True
    )

    queries = sorted(set(row["query"] for row in labels))

    for query in queries:
        original = rank_all(
            query, companies, model, embeddings,
            expanded=False
        )

        expanded = rank_all(
            query, companies, model, embeddings,
            expanded=True
        )

        print("\n" + "=" * 75)
        print("QUERY:", query)
        print("=" * 75)

        print(
            f"{'COMPANY':30} {'LABEL':15} "
            f"{'ORIGINAL':>10} {'EXPANDED':>10}"
        )

        for row in labels:
            if row["query"] != query:
                continue

            company_id = int(row["company_id"])

            print(
                f"{row['company_name'][:30]:30} "
                f"{row['ground_truth'][:15]:15} "
                f"{str(original.get(company_id, '-')):>10} "
                f"{str(expanded.get(company_id, '-')):>10}"
            )


if __name__ == "__main__":
    main()
