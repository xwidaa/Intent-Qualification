import re
from urllib.parse import urlparse


def normalize_name(name):
    """Normalize company names for comparison."""

    name = str(name or "").lower().strip()
    name = re.sub(r"[^\w\s]", " ", name)
    name = re.sub(r"\s+", " ", name)

    return name


def normalize_website(website):
    """Normalize company website domains."""

    if not website:
        return ""

    website = str(website).lower().strip()

    if not website.startswith(("http://", "https://")):
        website = "https://" + website

    domain = urlparse(website).hostname or ""
    domain = domain.removeprefix("www.")

    return domain


def deduplicate_results(results, companies):
    """Remove repeated companies from a ranked result list."""

    seen_websites = set()
    seen_names = set()
    unique_results = []

    for result in results:
        company = companies[result["company_id"]]

        website = normalize_website(
            company.get("website")
        )

        name = normalize_name(
            company.get("operational_name")
        )

        if website and website in seen_websites:
            continue

        if name and name in seen_names:
            continue

        unique_results.append(result)

        if website:
            seen_websites.add(website)

        if name:
            seen_names.add(name)

    return unique_results
