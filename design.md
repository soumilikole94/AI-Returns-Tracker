# AI Returns Tracker – Design

## Problem

Users often forget to return items they bought online before the deadline, losing money.

## Goal

Build an AI assistant that:
- Reads order-related emails (starting with Amazon).
- Extracts key information: store, items, prices, dates.
- Uses store return policies to compute the last allowed return date.
- Stores everything in a database.
- Sends reminders (7/3/1 days before deadline).
- Provides a dashboard + chat assistant to ask "What should I return this weekend?"

## High-level architecture

1. Ingestion & Extraction:
   - Connects to Gmail.
   - Fetches new emails.
   - Classifies them (order/shipping/delivery).
   - Uses an LLM to extract structured fields.

2. Policy RAG:
   - Stores retailer return policies in a vector database.
   - Uses embeddings + retrieval to find relevant policy snippets.
   - Infers return deadline when not explicit.

3. Reminder Engine:
   - Daily job that checks items with upcoming deadlines.
   - Sends reminder emails / calendar events.

4. UI & Agent:
   - Web/dashboard view of upcoming returns.
   - Chat interface backed by an LLM using tools (list returns, get policy, etc.).
