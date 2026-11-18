from sentence_transformers import CrossEncoder, SentenceTransformer

from src.data_loader import load_companies
from src.semantic_ranker import (
    MODEL_NAME,
    company_to_text
)
from src.hybrid_ranker import hybrid_rank


CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


def rerank_candidates(query, candidates, companies, cross_encoder):
    """Rerank retrieved candidates using a Cross-Encoder."""

    if not candidates:
        return []

    pairs = []

    for candidate in candidates:
        company = companies[candidate["company_id"]]

        pairs.append((
            query,
            company_to_text(company)
        ))

    scores = cross_encoder.predict(
        pairs,
        batch_size=16,
        show_progress_bar=False
    )

    reranked = []

    for candidate, score in zip(candidates, scores):
        reranked.append({
            **candidate,
            "cross_encoder_score": float(score)
        })

    reranked.sort(
        key=lambda item: item["cross_encoder_score"],
        reverse=True
    )

    return reranked


def main():
    companies = load_companies()

    print("Loading Bi-Encoder...")
    bi_encoder = SentenceTransformer(MODEL_NAME)

    print("Loading Cross-Encoder...")
    cross_encoder = CrossEncoder(CROSS_ENCODER_MODEL)

    print("Generating company embeddings...")

    embeddings = bi_encoder.encode(
        [company_to_text(c) for c in companies],
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

        candidates = hybrid_rank(
            query,
            companies,
            bi_encoder,
            embeddings,
            top_k=30
        )

        reranked = rerank_candidates(
            query,
            candidates,
            companies,
            cross_encoder
        )

        print("\n" + "=" * 70)
        print("QUERY:", query)
        print("=" * 70)

        for item in reranked[:10]:
            print(
                f"{str(item['name'])[:32]:32} "
                f"Cross: {item['cross_encoder_score']:.4f} "
                f"Semantic: {item['semantic_score']:.4f}"
            )


if __name__ == "__main__":
    main()
