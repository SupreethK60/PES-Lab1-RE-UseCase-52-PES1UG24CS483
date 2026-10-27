"""Insurance premium calculator used for Lab 5 static code analysis."""

from dataclasses import dataclass
from datetime import date, datetime
import math
import os
import secrets
import tarfile
import urllib.request

from defusedxml import ElementTree as SafeET


@dataclass(frozen=True)
class PolicyDetails:
    """Input details required to calculate an insurance premium."""

    policy_type: str
    age: int
    sum_insured: float
    smoker: bool
    claims: int


# In-memory quote book and application configuration.
quotes = {}
HOST = "127.0.0.1"
LOG_FILE = "premium_quotes.log"
BASE_RATES = {"health": 5000, "motor": 3000, "life": 8000}


def calculate_premium(policy, discounts=None):
    """Calculate a premium without mutating caller-owned discount data."""
    if policy.policy_type not in BASE_RATES:
        raise ValueError(f"Unknown policy type: {policy.policy_type!r}")
    if policy.age < 0 or policy.sum_insured < 0 or policy.claims < 0:
        raise ValueError("Age, sum insured, and claims must be non-negative")

    applied_discounts = [] if discounts is None else list(discounts)
    if any(discount < 0 for discount in applied_discounts):
        raise ValueError("Discounts must be non-negative")

    premium = BASE_RATES[policy.policy_type] + policy.sum_insured * 0.002
    if policy.age > 45:
        premium *= 1.5
    if policy.smoker:
        premium *= 1.3
    premium += policy.claims * 1000
    for discount in applied_discounts:
        premium -= discount
    return max(0.0, premium)


def age_from_dob(dob):
    """Return age in years for a date written as DD-MM-YYYY."""
    born = datetime.strptime(dob, "%d-%m-%Y").date()
    today = date.today()
    if born > today:
        raise ValueError("Date of birth cannot be in the future")
    return today.year - born.year - (
        (today.month, today.day) < (born.month, born.day)
    )


def policy_number():
    """Generate a quote identifier using a cryptographically secure source."""
    return f"POL-{secrets.randbelow(900000) + 100000}"


def save_quote(name, premium):
    """Save a quote in memory and append it to the log file."""
    number = policy_number()
    quotes[number] = {"name": name, "premium": premium}
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(f"{number},{name},{premium:.2f}\n")
    return number


def import_policies(xml_text):
    """Parse partner policy XML safely, skipping malformed policy entries."""
    root = SafeET.fromstring(xml_text)
    result = []
    for policy_element in root.findall("policy"):
        try:
            policy_type = policy_element.get("type")
            age_text = policy_element.get("age")
            sum_text = policy_element.get("sum")
            if (
                policy_type not in BASE_RATES
                or age_text is None
                or sum_text is None
            ):
                continue
            age = int(age_text)
            sum_insured = float(sum_text)
            if age < 0 or sum_insured < 0:
                continue
            result.append((policy_type, age, sum_insured))
        except (TypeError, ValueError):
            continue
    return result


def fetch_rates(url, timeout=10):
    """Fetch rate data over HTTPS with certificate verification enabled."""
    if not url.lower().startswith("https://"):
        raise ValueError("Rate table URL must use HTTPS")
    # HTTPS is enforced above; certificate verification stays enabled.
    request = urllib.request.Request(url)
    # Bandit's B310 check is suppressed for this validated HTTPS-only call.
    with urllib.request.urlopen(  # nosec B310
        request, timeout=timeout
    ) as response:
        return response.read()


def import_claim_documents(archive_path):
    """Extract only regular files and directories from a tar archive safely."""
    destination = os.path.abspath("claims_docs")
    os.makedirs(destination, exist_ok=True)
    destination_prefix = destination + os.sep

    with tarfile.open(archive_path, "r:*") as archive:
        members = archive.getmembers()
        for member in members:
            target = os.path.abspath(
                os.path.join(destination, member.name)
            )
            is_outside_destination = (
                not target.startswith(destination_prefix)
                and target != destination
            )
            if is_outside_destination:
                raise ValueError(f"Unsafe archive path: {member.name!r}")
            if not member.isfile() and not member.isdir():
                raise ValueError(f"Unsupported archive entry: {member.name!r}")
        archive.extractall(destination, members=members, filter="data")


def monthly_instalment(premium, months=12):
    """Calculate a monthly instalment using whole currency units."""
    if months <= 0:
        raise ValueError("Months must be greater than zero")
    if premium < 0:
        raise ValueError("Premium must be non-negative")
    return math.floor(premium / months)


def is_authorised(token):
    """Compare a supplied token against the configured environment secret."""
    expected_token = os.environ.get("UNDERWRITER_TOKEN")
    if not expected_token:
        return False
    return secrets.compare_digest(token, expected_token)


def renewal_due(start, years=1):
    """Return the renewal date, handling leap-day dates safely."""
    if years < 0:
        raise ValueError("Years must be non-negative")
    start_date = datetime.strptime(start, "%Y-%m-%d").date()
    try:
        renewed = start_date.replace(year=start_date.year + years)
    except ValueError:
        renewed = start_date.replace(
            month=2, day=28, year=start_date.year + years
        )
    return renewed.strftime("%Y-%m-%d")


def print_quotes():
    """Print quotes currently stored in the in-memory quote book."""
    print("===== Quote Book =====")
    for index, (number, quote) in enumerate(quotes.items(), start=1):
        print(index, number, quote["name"], "Rs.", quote["premium"])


def main():
    """Run a demonstration of the calculator's functions."""
    standard_health = PolicyDetails("health", 30, 500000, False, 0)
    older_motor = PolicyDetails("motor", 50, 800000, False, 0)
    discounted_life = PolicyDetails("life", 25, 100000, False, 0)

    premium_one = calculate_premium(standard_health)
    premium_two = calculate_premium(standard_health)
    premium_three = calculate_premium(older_motor)
    premium_four = calculate_premium(
        discounted_life, discounts=[3000, 3000, 3000]
    )

    print("Quote 1:", premium_one)
    print("Quote 2 (same customer details):", premium_two)
    print("Non-smoker aged 50:", premium_three)
    print("Life with stacked discounts:", premium_four)
    print("Age from DOB 31-12-1990:", age_from_dob("31-12-1990"))
    print("Monthly instalment:", monthly_instalment(premium_three))
    print("Renewal due:", renewal_due("2025-03-15"))
    xml_text = (
        "<policies><policy type='health' age='40' sum='300000'/>"
        "<policy type='motor' age='abc' sum='1'/></policies>"
    )
    print("Imported:", import_policies(xml_text))
    print("Saved as:", save_quote("Kiran", premium_one))
    token = os.environ.get("UNDERWRITER_TOKEN", "")
    print("Authorised:", is_authorised(token))
    print("Server would listen on", HOST)
    print_quotes()


if __name__ == "__main__":
    main()
