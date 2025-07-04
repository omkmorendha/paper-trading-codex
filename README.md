# Paper Trading Codex

This repository contains a simple paper trading web application for Indian stocks. It uses FastAPI for the backend and React for the frontend. Authentication is handled by Supabase.

- **backend** – FastAPI app with endpoints for retrieving stock prices and placing paper trades. Stock data is retrieved from Alpha Vantage if an API key is provided, otherwise `yfinance` is used.
- **frontend** – React application that signs users in with Supabase and communicates with the backend.

## Running locally

### Backend

```bash
cd backend
uv pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Fill in environment variables as described in `frontend/.env.example` and `backend/README.md`.
