# Backend

This directory contains a FastAPI app for the paper trading web application.

## Running locally

```bash
uv pip install -r requirements.txt
uvicorn app.main:app --reload
```

Environment variables:
- `ALPHAVANTAGE_KEY` (optional): API key for Alpha Vantage.
- `SUPABASE_URL` and `SUPABASE_KEY`: credentials for Supabase project.

If `ALPHAVANTAGE_KEY` is not provided, the service will fall back to using `yfinance` to fetch stock data.
