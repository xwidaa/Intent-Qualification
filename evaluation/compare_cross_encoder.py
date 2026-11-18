import csv
import time

from sentence_transformers import SentenceTransformer, CrossEncoder

from src.data_loader import load_companies
from src.semantic_ranker import MODEL_NAME, company_to_text
from src.hybrid_ranker import hybrid_rank
from src.cross_encoder_ranker import (
    CROSS_ENCODER_MODEL,
    rerank_candidates
)


QUERIES = [
    "Logistic companies in Romania",
    "Public software companies with more than 1,000 employees",
    "Clean energy startups founded after 2018 with fewer than 200 employees",
    "Companies supplying packaging materials for cosmetics brands"
]


def load_labels():
    labels = {}

    with open(
        "evaluation/labels_enriched.csv",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        for row in csv.DictReader(file):
            if row["ground_truth"]:
                key = (row["query"], int(row["company_id"]))
                labels[key] = row["ground_truth"]

    return labels


def compare():
    companies = load_companies()
    labels = load_labels()

    print("Loading models...")

    bi_encoder = SentenceTransformer(MODEL_NAME)
    cross_encoder = CrossEncoder(CROSS_ENCODER_MODEL)

    embeddings = bi_encoder.encode(
        [company_to_text(c) for c in companies],
        normalize_embeddings=True,
        batch_size=32,
        show_progress_bar=True
    )

    for query in QUERIES:
        candidates = hybrid_rank(
            query,
            companies,
            bi_encoder,
            embeddings,
            top_k=30
        )

        start = time.perf_counter()

        reranked = rerank_candidates(
            query,
            candidates,
            companies,
            cross_encoder
        )

        duration = time.perf_counter() - start

        original_positions = {
            item["company_id"]: index
            for index, item in enumerate(candidates, 1)
        }

        reranked_positions = {
            item["company_id"]: index
            for index, item in enumerate(reranked, 1)
        }

        print("\n" + "=" * 75)
        print("QUERY:", query)
        print(f"Candidates: {len(candidates)}")
        print(f"Cross-Encoder time: {duration:.3f}s")

        print(
            f"\n{'COMPANY':30} {'LABEL':15} "
            f"{'BEFORE':>8} {'AFTER':>8}"
        )

        found = 0

        for (label_query, company_id), label in labels.items():
            if label_query != query:
                continue

            before = original_positions.get(company_id)
            after = reranked_positions.get(company_id)

            if before is None:
                continue

            found += 1

            print(
                f"{str(companies[company_id].get('operational_name'))[:30]:30} "
                f"{label[:15]:15} "
                f"{before:>8} {after:>8}"
            )

        print(f"\nLabeled candidates in pool: {found}")

        print("\nTOP 5 AFTER RERANKING:")

        for item in reranked[:5]:
            print(
                f"{item['name']} "
                f"| Cross: {item['cross_encoder_score']:.4f}"
            )


if __name__ == "__main__":
    compare()
