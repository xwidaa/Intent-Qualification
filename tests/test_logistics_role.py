import unittest

from src.logistics_role import evaluate_logistics_role


class TestLogisticsRole(unittest.TestCase):

    def test_port_services(self):
        company = {
            "core_offerings": [
                "Maritime and River Port Services",
                "Dry Bulk Cargo Handling and Transshipment"
            ]
        }

        result = evaluate_logistics_role(company)

        self.assertEqual(result["status"], "MATCH")

    def test_support_services_not_logistics(self):
        company = {
            "core_offerings": [
                "Technical Support Services",
                "HR Software Support Services"
            ]
        }

        result = evaluate_logistics_role(company)

        self.assertEqual(result["status"], "UNKNOWN")

    def test_freight_transport(self):
        company = {
            "core_offerings": [
                "Freight Rail Transport Services"
            ]
        }

        result = evaluate_logistics_role(company)

        self.assertEqual(result["status"], "MATCH")


if __name__ == "__main__":
    unittest.main()
