from pprint import pprint

from app.ingestion.email_fetcher import load_sample_emails
from app.ingestion.email_parser import parse_email_to_order


def run_demo():
    emails = load_sample_emails()
    print(f"Found {len(emails)} sample emails.\n")

    for email in emails:
        print("=" * 80)
        print(f"Filename: {email['filename']}")
        print("-" * 80)

        try:
            order_data = parse_email_to_order(email["raw_text"])
        except Exception as e:
            print(f"Error parsing email {email['filename']}: {e}")
            continue

        print("Extracted order data:")
        pprint(order_data)
        print("\n")


if __name__ == "__main__":
    run_demo()
