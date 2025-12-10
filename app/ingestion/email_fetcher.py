import os
from pathlib import Path
from typing import List, Dict


def load_sample_emails(base_dir: str = "data/sample_emails") -> List[Dict]:
    """
    Load all .txt sample emails from the given directory.

    Returns a list of dicts:
    [
      {
        "filename": "amazon_order_1_explicit_deadline.txt",
        "subject": "...",   # optional, we can parse later
        "raw_text": "full file contents ..."
      },
      ...
    ]
    """
    base_path = Path(base_dir)
    if not base_path.exists():
        raise FileNotFoundError(f"Sample email directory not found: {base_dir}")

    emails: List[Dict] = []

    for file_path in base_path.glob("*.txt"):
        with file_path.open("r", encoding="utf-8") as f:
            text = f.read()

        emails.append(
            {
                "filename": file_path.name,
                "raw_text": text,
            }
        )

    return emails


if __name__ == "__main__":
    # This lets you run the file directly with:
    # python -m app.ingestion.email_fetcher
    emails = load_sample_emails()
    print(f"Loaded {len(emails)} emails:")
    for e in emails:
        print("-" * 40)
        print(f"Filename: {e['filename']}")
        # print only first 200 chars to keep it short
        preview = e["raw_text"][:200].replace("\n", " ")
        print(f"Preview: {preview}...")
