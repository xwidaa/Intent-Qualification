from src.data_loader import load_companies


COMPANY_IDS = [
    59, 62, 54, 53, 61,
    57, 55, 56, 23, 51
]


def main():
    companies = load_companies()

    print("\n=== FINTECH COMPANY ANALYSIS ===")

    for company_id in COMPANY_IDS:
        company = companies[company_id]

        print("\n" + "=" * 65)
        print("ID:", company_id)
        print("Company:", company.get("operational_name"))
        print("Primary NAICS:", company.get("primary_naics"))
        print("Business model:", company.get("business_model"))
        print("Core offerings:", company.get("core_offerings"))
        print("Target markets:", company.get("target_markets"))
        print("Description:", company.get("description"))
        print("Year founded:", company.get("year_founded"))
        print("Employees:", company.get("employee_count"))
        print("Revenue:", company.get("revenue"))


if __name__ == "__main__":
    main()
