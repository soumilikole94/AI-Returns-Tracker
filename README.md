# AI-Returns-Tracker
AI assistant that tracks online purchases and reminds the user before return deadlines

## What it does
- Connects to the user's email (starting with Amazon).
- Detects order confirmation emails.
- Extracts order details (items, prices, dates).
- Infers return deadlines using store policies.
- Reminds user a week/ few days before the user loses the chance to return, and how much money is at stake for that return.

## Tech stack
- Python
- FastAPI (backend API)
- RAG over retailer return policies
- LLMs (for email understanding and policy interpretation)
- Postgres / SQLite for storage
- (Later) Streamlit / simple web UI

## Status
Early scaffold. More features coming soon.
