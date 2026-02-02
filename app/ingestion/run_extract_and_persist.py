from pprint import pprint

from app.ingestion.email_fetcher import load_sample_emails
from app.ingestion.email_parser import parse_email_to_order
from app.ingestion.persist_extracted import upsert_order
from app.ingestion.email_classifier import classify_email



def main():
    emails = load_sample_emails()
    print(f"Found {len(emails)} sample emails")

    for email in emails:
        email_type = classify_email(email["raw_text"])
        print(f"Classified as: {email_type}")

        if email_type != "ORDER_CONFIRMATION":
            print("Skipping extraction/persist (not an order confirmation).")
            continue

        print("=" * 80)
        print(f"Filename: {email['filename']}")
        extracted = parse_email_to_order(email["raw_text"])
        order_db_id = upsert_order(extracted)
        print(f"Saved order to DB with id={order_db_id}")
        pprint(extracted)

    print("\nDone. Your data is now in local.db")


if __name__ == "__main__":
    main()
