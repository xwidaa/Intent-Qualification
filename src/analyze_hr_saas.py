from src.data_loader import load_companies


COMPANY_IDS = [66, 89, 81, 85, 108, 64, 95]


def main():
    companies = load_companies()

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


if __name__ == "__main__":
    main()
