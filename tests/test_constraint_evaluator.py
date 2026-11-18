import unittest

from src.constraint_evaluator import (
    evaluate_company,
    numeric_check
)
from src.query_parser import parse_query


class TestConstraintEvaluator(unittest.TestCase):

    def test_revenue_above_threshold(self):
        company = {
            "operational_name": "Example Construction",
            "address": {"country_code": "us"},
            "revenue": 75_000_000
        }

        query = (
            "Construction companies in the United States "
            "with revenue over $50 million"
        )

        result = evaluate_company(company, parse_query(query))

        self.assertEqual(
            result["checks"]["min_revenue"], "MATCH"
        )
        self.assertEqual(
            result["checks"]["country"], "MATCH"
        )
        self.assertEqual(result["status"], "UNKNOWN")

    def test_revenue_below_threshold(self):
        company = {
            "address": {"country_code": "us"},
            "revenue": 30_000_000
        }

        query = (
            "Construction companies in the United States "
            "with revenue over $50 million"
        )

        result = evaluate_company(company, parse_query(query))

        self.assertEqual(result["status"], "NO_MATCH")

    def test_missing_employees(self):
        self.assertEqual(
            numeric_check(None, 1000, "gt"),
            "UNKNOWN"
        )

    def test_scandinavia(self):
        query = (
            "Renewable energy equipment manufacturers "
            "in Scandinavia"
        )

        constraints = parse_query(query)

        sweden = {
            "address": {"country_code": "se"}
        }

        finland = {
            "address": {"country_code": "fi"}
        }

        result_se = evaluate_company(sweden, constraints)
        result_fi = evaluate_company(finland, constraints)

        self.assertEqual(
            result_se["checks"]["region"], "MATCH"
        )

        self.assertEqual(
            result_fi["checks"]["region"], "NO_MATCH"
        )


if __name__ == "__main__":
    unittest.main()
