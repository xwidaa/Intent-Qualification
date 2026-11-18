import csv
from collections import defaultdict

FILE_PATH = "evaluation/manual_review.csv"


def main():
    with open(FILE_PATH, "r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    groups = defaultdict(list)

    for row in rows:
        groups[int(row["query_id"])].append(row)

    total_relevant = 0
    total_not_relevant = 0
    total_uncertain = 0

    print("QUERY EVALUATION")
    print("=" * 65)

    for query_id in sorted(groups):
        group = groups[query_id]

        relevant = sum(r["manual_label"] == "RELEVANT" for r in group)
        not_relevant = sum(r["manual_label"] == "NOT_RELEVANT" for r in group)
        uncertain = sum(r["manual_label"] == "UNCERTAIN" for r in group)

        total_relevant += relevant
        total_not_relevant += not_relevant
        total_uncertain += uncertain

        n = len(group)

        lower_bound = relevant / n
        upper_bound = (relevant + uncertain) / n

        print(
            f"Query {query_id:2d}: "
            f"Relevant={relevant:2d}, "
            f"Not Relevant={not_relevant:2d}, "
            f"Uncertain={uncertain:2d}, "
            f"P@{n} bounds={lower_bound:.2%}-{upper_bound:.2%}"
        )

    total = len(rows)

    print("\nOVERALL RESULTS")
    print("=" * 65)
    print("Total results:", total)
    print("Relevant:", total_relevant)
    print("Not relevant:", total_not_relevant)
    print("Uncertain:", total_uncertain)

    print(
        "Overall precision lower bound:",
        f"{total_relevant / total:.2%}"
    )
    print(
        "Overall precision upper bound:",
        f"{(total_relevant + total_uncertain) / total:.2%}"
    )

    print(
        "Review coverage:",
        f"{(total_relevant + total_not_relevant) / total:.2%}"
    )


if __name__ == "__main__":
    main()
