from src.query_parser import parse_query


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


def test_query_parsing():
    print("\n=== QUERY PARSING COVERAGE ===")

    for index, query in enumerate(QUERIES, start=1):
        parsed = parse_query(query)

        identified = {
            key: value
            for key, value in parsed.items()
            if value is not None
        }

        print(f"\nQuery {index}: {query}")
        print("Identified constraints:", identified)


if __name__ == "__main__":
    test_query_parsing()
