import numpy as np
from sentence_transformers import SentenceTransformer

from src.data_loader import load_companies


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def company_to_text(company):
    """Build a semantic representation of a company."""

    naics = company.get("primary_naics") or {}

    offerings = company.get("core_offerings") or []
    markets = company.get("target_markets") or []

    return " ".join([
        str(naics.get("label", "")),
        str(company.get("description") or ""),
        " ".join(map(str, offerings)),
        " ".join(map(str, markets))
    ])


def rank_companies(query, companies, model, embeddings, top_k=10):
    """Rank companies by cosine similarity."""

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )[0]

    scores = embeddings @ query_embedding

    ranked_indices = np.argsort(scores)[::-1][:top_k]

    return [
        {
            "company_id": int(index),
            "name": companies[index].get("operational_name"),
            "score": float(scores[index])
        }
        for index in ranked_indices
    ]


def main():
    companies = load_companies()

    texts = [
        company_to_text(company)
        for company in companies
    ]

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Generating company embeddings...")
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True,
        batch_size=32
    )

    queries = [
        "Logistic companies in Romania",
        "Public software companies with more than 1,000 employees",
        "Clean energy startups founded after 2018 with fewer than 200 employees",
        "Companies supplying packaging materials for cosmetics brands"
    ]

    for query in queries:
        print("\n" + "=" * 65)
        print("QUERY:", query)
        print("=" * 65)

        results = rank_companies(
            query, companies, model, embeddings
        )

        for result in results:
            print(
                f"{result['name'][:35]:35} "
                f"Similarity: {result['score']:.4f}"
            )


if __name__ == "__main__":
    main()
