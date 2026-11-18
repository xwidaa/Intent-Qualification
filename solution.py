import csv
import time
from pathlib import Path

from sentence_transformers import SentenceTransformer

from src.data_loader import load_companies
from src.query_parser import parse_query
from src.constraint_evaluator import evaluate_company
from src.business_role import (
    evaluate_business_role,
    PRODUCT_PATTERNS
)
from src.semantic_ranker import MODEL_NAME, company_to_text
from src.deduplication import deduplicate_results

from src.logistics_role import evaluate_logistics_provider
from src.hr_saas_evidence import evaluate_hr_saas
from src.fintech_evidence import evaluate_fintech

QUERIES = [
    "Logistic companies in Romania",
    "Public software companies with more than 1,000 employees",
    "Food and beverage manufacturers in France",
    "Companies that could supply packaging materials for a direct-to-consumer cosmetics brand",
    "Construction companies in the United States with revenue over $50 million",
    "Pharmaceutical companies in Switzerland",
    "B2B SaaS companies providing HR solutions in Europe",
    "Clean energy startups founded after 2018 with fewer than 200 employees",
    "Fast-growing fintech companies competing with traditional banks in Europe",
    "E-commerce companies using Shopify or similar platforms",
    "Renewable energy equipment manufacturers in Scandinavia",
    "Companies that manufacture or supply critical components for electric vehicle battery production"
]


class IntentQualificationSystem:

    def __init__(self):
        print("Loading companies...")
        self.companies = load_companies()

        print("Loading embedding model...")
        self.model = SentenceTransformer(MODEL_NAME)

        print("Generating company embeddings...")
        self.embeddings = self.model.encode(
            [company_to_text(c) for c in self.companies],
            normalize_embeddings=True,
            batch_size=32,
            show_progress_bar=True
        )

    def qualify(self, query, top_k=10):
        constraints = parse_query(query)

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )[0]

        scores = self.embeddings @ query_embedding

        candidates = []

        for index, company in enumerate(self.companies):

            structured = evaluate_company(
                company, constraints
            )

            if structured["status"] == "NO_MATCH":
                continue

            role_result = evaluate_business_role(
                company, constraints
            )

            product_category = constraints.get(
                "product_category"
            )

            has_role_evidence = (
                product_category in PRODUCT_PATTERNS
                and role_result["status"] == "MATCH"
            )

            evidence = [
                item["offering"]
                for item in role_result["evidence"]
            ]


            logistics_status = None

            if constraints.get("industry") == "logistics":
                logistics_result = evaluate_logistics_provider(
                    company
                )

                logistics_status = logistics_result["status"]

                if logistics_status == "STRONG_MATCH":
                    evidence.extend(
                        logistics_result["service_evidence"]
                    )


            hr_saas_status = None

            if product_category == "hr_software":
                hr_result = evaluate_hr_saas(company)

                hr_saas_status = hr_result["status"]

                if hr_saas_status == "STRONG_MATCH":
                    evidence.extend(hr_result["evidence"])


            fintech_status = None

            if constraints.get("industry") == "fintech":
                fintech_result = evaluate_fintech(company)

                fintech_status = fintech_result["status"]

                if fintech_status == "STRONG_MATCH":
                    evidence.extend(
                        fintech_result["fintech_evidence"]
                    )
                    evidence.extend(
                        fintech_result["banking_evidence"]
                    )

                    evidence = list(dict.fromkeys(evidence))


            limitations = []

            if constraints.get("industry") == "ecommerce":
                limitations.append(
                    "E-commerce platform usage cannot be "
                    "verified from the available company data."
                )

            if constraints.get("industry") == "fintech":
                limitations.append(
                    "Fast growth cannot be verified from "
                    "the available company data."
                )


            checks = structured["checks"].copy()

            if logistics_status == "STRONG_MATCH":
                checks["industry"] = "MATCH"
                checks["business_role"] = "MATCH"

            if hr_saas_status == "STRONG_MATCH":
                checks["business_model_b2b"] = "MATCH"
                checks["business_model_saas"] = "MATCH"
                checks["product_category"] = "MATCH"
                checks["business_role"] = "MATCH"

            if fintech_status == "STRONG_MATCH":
                checks["industry"] = "MATCH"
                checks["business_role"] = "MATCH"
                checks["fast_growing"] = "UNKNOWN"

            if has_role_evidence:
                checks["product_category"] = "MATCH"
                checks["business_role"] = "MATCH"

            candidates.append({
                "company_id": index,
                "name": (
                    company.get("operational_name")
                    or company.get("website")
                    or f"Company {index}"
                ),
                "semantic_score": float(scores[index]),
                "has_role_evidence": has_role_evidence,
                "evidence": evidence,
                "checks": checks,

                "qualification_status": (
                    "EVIDENCE_FOUND"
                    if (
                        has_role_evidence
                        or logistics_status == "STRONG_MATCH"
                        or hr_saas_status == "STRONG_MATCH"
                        or fintech_status == "STRONG_MATCH"
                    )
                    else "UNVERIFIED"
                ),

                "limitations": limitations,
                "logistics_status": logistics_status,
                "hr_saas_status": hr_saas_status,
                "fintech_status": fintech_status
            })


        structured_keys = {
            "country",
            "region",
            "is_public",
            "min_employees",
            "max_employees",
            "min_revenue",
            "founded_after",
        }




        def ranking_key(item):
            checks = item["checks"]

            unknown_structured = sum(
                1
                for key, status in checks.items()
                if key in structured_keys
                and status == "UNKNOWN"
            )

            strong_match = any(
                item.get(key) == "STRONG_MATCH"
                for key in (
                    "logistics_status",
                    "hr_saas_status",
                    "fintech_status"
                )
            )

            return (
                int(strong_match),
                int(item["has_role_evidence"]),
                -unknown_structured,
                item["semantic_score"]
            )




        candidates.sort(
            key=ranking_key,
            reverse=True
        )


        unique_candidates = deduplicate_results(
            candidates,
            self.companies
        )

        return unique_candidates[:top_k]


def main():
    system = IntentQualificationSystem()

    output_rows = []
    output_path = Path("results/results.csv")
    output_path.parent.mkdir(
        parents=True, exist_ok=True
    )

    for query_id, query in enumerate(QUERIES, start=1):
        start = time.perf_counter()

        results = system.qualify(query)

        duration = time.perf_counter() - start

        print("\n" + "=" * 75)
        print(f"QUERY {query_id}: {query}")
        print(f"Ranking time: {duration:.3f}s")
        print("=" * 75)

        for rank, result in enumerate(results, start=1):
            print(
                f"{rank:2}. {result['name'][:35]:35} "
                f"Similarity: {result['semantic_score']:.4f} "
                f"| {result['qualification_status']}"
            )

            if result["evidence"]:
                print(
                    "    Evidence:",
                    result["evidence"][0]
                )

            if result["limitations"]:
                print(
                    "    Limitations:",
                    "; ".join(result["limitations"])
                    )

            output_rows.append({
                "query_id": query_id,
                "query": query,
                "rank": rank,
                "company_id": result["company_id"],
                "company_name": result["name"],
                "semantic_score": round(
                    result["semantic_score"], 4
                ),
                "qualification_status": (
                    result["qualification_status"]
                ),
                "evidence": "; ".join(
                    result["evidence"]
                ),
                "constraint_checks": str(
                    result["checks"]
                ),
                "limitations": "; ".join(result["limitations"])
            })

    with open(
        output_path,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "query_id",
                "query",
                "rank",
                "company_id",
                "company_name",
                "semantic_score",
                "qualification_status",
                "evidence",
                "constraint_checks",
                "limitations"
            ]
        )

        writer.writeheader()
        writer.writerows(output_rows)

    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
