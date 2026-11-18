# Intent Qualification

A Python-based company qualification system that interprets natural-language business queries, filters company records using structured constraints, and ranks potential matches using semantic similarity and business-specific evidence.

## 1. Overview

The goal of this project is to identify companies that match different business intents, such as finding suppliers, manufacturers, logistics providers, or software companies.

The dataset contains 477 company records, including company descriptions, industries, business models, geographic locations, financial information, and core offerings.

The system processes 12 predefined queries and returns the top 10 companies for each query.

Rather than relying only on keyword matching, the solution combines:

- Natural-language query parsing
- Structured constraint evaluation
- Semantic similarity ranking
- Business-role evidence detection
- Result deduplication
- Explicit handling of missing information

## 2. Approach

### Query parsing

Each query is converted into structured requirements.

Depending on the query, these may include:

- Industry or product category
- Country or geographic region
- Public company status
- Minimum or maximum employee count
- Minimum revenue
- Founding year
- Business model
- Supplier or manufacturer role

### Constraint evaluation

Structured company attributes are checked against the query requirements.

Each constraint can receive one of three statuses:

- MATCH: The available data supports the requirement.
- NO_MATCH: The available data contradicts the requirement.
- UNKNOWN: The requirement cannot be verified.

Companies with confirmed hard-constraint violations are excluded.

### Semantic ranking

The system uses the `sentence-transformers/all-MiniLM-L6-v2` model to generate embeddings.

Company representations are built from their industry classification, core offerings, business model information, and descriptive text.

Cosine similarity, computed through normalized embedding vectors, helps identify companies whose activities are semantically related to the query.

### Business-role evidence

Additional rule-based checks identify evidence for specific business intents:

- Logistics providers
- Cosmetics packaging suppliers
- Renewable energy equipment manufacturers
- EV battery component suppliers
- B2B HR SaaS providers
- Fintech services

These checks help distinguish companies performing the requested activity from companies that merely mention related terminology.

### Deduplication

The final ranking removes duplicate company entries using available identifying information.

## 3. Project Structure

```text
data/
    companies.jsonl

src/
    data_loader.py
    query_parser.py
    constraint_evaluator.py
    semantic_ranker.py
    deduplication.py
    business_role.py
    logistics_role.py
    hr_saas_evidence.py
    fintech_evidence.py
    platform_evidence.py

evaluation/
    manual_review.csv
    create_review_file.py
    review_query.py
    metrics.py

results/
    results.csv

tests/
    test_constraint_evaluator.py
    test_logistics_role.py
    test_query_parser.py

solution.py
requirements.txt
README.md
```

Additional experimental scripts are included for investigating alternative ranking and evaluation approaches. They are not required by the main qualification pipeline.

## 4. Installation

Python 3.10 or newer is recommended.

Clone the repository and navigate to the project directory.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

The embedding model is downloaded automatically on the first execution. An internet connection is required for the initial download.

## 5. Running the Solution

From the project root, execute:

```bash
python solution.py
```

The program:

1. Loads the company dataset.
2. Initializes the sentence embedding model.
3. Generates company embeddings.
4. Processes the 12 business queries.
5. Evaluates structured constraints and business evidence.
6. Ranks and deduplicates candidate companies.
7. Saves the results to `results/results.csv`.

The generated CSV contains:

- Query ID and query text
- Result rank
- Company ID and company name
- Semantic similarity score
- Qualification status
- Supporting evidence
- Constraint evaluation details
- Known limitations

The qualification status indicates whether supporting evidence was identified. It does not guarantee that every condition in the query has been independently verified.

## 6. Evaluation

The system was evaluated using the top 10 results for each of the 12 queries.

A total of 120 query-company results were manually reviewed against the available company profiles.

Three evaluation labels were used:

- RELEVANT: The available information supports the query requirements.
- NOT_RELEVANT: The profile does not satisfy the intended business requirement.
- UNCERTAIN: At least one important requirement cannot be established from the available data.

### Evaluation results

| Metric | Result |
|---|---:|
| Queries evaluated | 12 |
| Retrieved results reviewed | 120 |
| Relevant | 80 |
| Not relevant | 14 |
| Uncertain | 26 |
| Precision lower bound | 66.67% |
| Precision upper bound | 88.33% |
| Definitively labeled proportion | 78.33% |

The precision interval treats uncertain results as incorrect in the lower bound and correct in the upper bound.

These numbers describe the retrieved results only. They should not be interpreted as dataset-wide recall or as externally verified accuracy.

The manual assessment was based on the supplied company profiles, so the evaluation is exploratory rather than an independent ground-truth benchmark.

To reproduce the evaluation summary:

```bash
python -m evaluation.metrics
```

### Observations

The system produced strong matches for queries involving clearly defined manufacturing activities, packaging suppliers, pharmaceuticals, and HR software.

More ambiguous queries were challenging.

For example:

- Logistics-related terms can appear in the profiles of manufacturers and distributors that are not logistics providers.
- The term "startup" cannot always be established from company age and employee count alone.
- Fast growth requires historical performance data that is not available in the dataset.
- Shopify or equivalent platform usage cannot be confirmed without platform-specific evidence.

These cases demonstrate the importance of distinguishing semantic relevance from verified business qualification.

## 7. Testing

Unit tests cover selected constraint evaluation and logistics classification scenarios.

Run the tests using:

```bash
python -m unittest discover -s tests -v
```

The latest verified execution completed successfully with 7 passing tests.

The end-to-end solution also completed successfully, generating 120 results across 12 queries.

## 8. Limitations

The current implementation has several limitations:

1. Missing or incomplete fields can prevent definitive qualification.
2. Semantic similarity may rank companies that discuss an industry without operating primarily in that industry.
3. The rule-based business evidence modules cover selected intents rather than all possible industries.
4. Business attributes such as rapid growth, startup status, or technology platform usage may require external verification.
5. The evaluation uses a limited dataset and manually assessed retrieved results.

The system intentionally exposes uncertainty instead of converting missing evidence into unsupported positive claims.

## 9. Future Improvements

Possible extensions include:

- More comprehensive query parsing
- Additional business-role detectors
- Better negative evidence handling
- External verification for missing company attributes
- Improved ranking for ambiguous industries
- More extensive unit and integration tests
- Evaluation using a larger independently labeled benchmark

## 10. Conclusion

This project demonstrates a hybrid approach to company qualification.

Structured constraints provide explicit filtering, semantic embeddings enable flexible matching, and business-specific evidence checks improve the interpretation of company roles.

A key design decision is to preserve uncertainty when the dataset does not contain enough evidence to confirm a business requirement.
