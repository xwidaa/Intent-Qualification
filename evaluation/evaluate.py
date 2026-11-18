import csv
from collections import Counter
from pathlib import Path

from src.data_loader import load_companies
from src.filters import filter_companies


LABELS_PATH = Path("evaluation/labels_enriched.csv")


def load_labels():
    with open(
        LABELS_PATH,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        return list(csv.DictReader(file))


def calculate_metrics(y_true, y_pred):
    tp = sum(
        truth == 1 and pred == 1
        for truth, pred in zip(y_true, y_pred)
    )

    fp = sum(
        truth == 0 and pred == 1
        for truth, pred in zip(y_true, y_pred)
    )

    fn = sum(
        truth == 1 and pred == 0
        for truth, pred in zip(y_true, y_pred)
    )

    tn = sum(
        truth == 0 and pred == 0
        for truth, pred in zip(y_true, y_pred)
    )

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0.0
    )

    return {
        "TP": tp,
        "FP": fp,
        "FN": fn,
        "TN": tn,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


def main():
    companies = load_companies()
    labels = load_labels()

    labeled = [
        row for row in labels
        if row["ground_truth"] in {
            "RELEVANT", "NOT_RELEVANT"
        }
    ]

    print(f"Total labeled examples: {len(labels)}")
    print(f"Examples with certain labels: {len(labeled)}")

    all_truth = []
    all_pred = []

    predictions_cache = {}

    for row in labeled:
        query = row["query"]
        company_id = int(row["company_id"])

        if query not in predictions_cache:
            predictions_cache[query] = filter_companies(
                companies, query
            )

        result = predictions_cache[query][company_id]

        truth = (
            1 if row["ground_truth"] == "RELEVANT"
            else 0
        )

        prediction = (
            1 if result["status"] == "MATCH"
            else 0
        )

        all_truth.append(truth)
        all_pred.append(prediction)


    print("\n=== FALSE POSITIVES ===")

    for row in labeled:
        query = row["query"]
        company_id = int(row["company_id"])

        result = predictions_cache[query][company_id]

        if (
            row["ground_truth"] == "NOT_RELEVANT"
            and result["status"] == "MATCH"
        ):
            print(f"\nCompany: {row['company_name']}")
            print(f"Query: {query}")
            print(f"Checks: {result['checks']}")
            print(f"Reason: {row['notes']}")

    print("\n=== FALSE NEGATIVES ===")

    for row in labeled:
        query = row["query"]
        company_id = int(row["company_id"])

        result = predictions_cache[query][company_id]

        if (
            row["ground_truth"] == "RELEVANT"
            and result["status"] != "MATCH"
        ):
            print(f"\nCompany: {row['company_name']}")
            print(f"Query: {query}")
            print(f"Checks: {result['checks']}")


    metrics = calculate_metrics(all_truth, all_pred)

    print("\n=== RULE-BASED BASELINE ===")

    for name, value in metrics.items():
        if name in {"precision", "recall", "f1"}:
            print(f"{name}: {value:.4f}")
        else:
            print(f"{name}: {value}")


if __name__ == "__main__":
    main()
