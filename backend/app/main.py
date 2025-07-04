import os
import requests
import yfinance as yf
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client

ALPHAVANTAGE_KEY = os.getenv("ALPHAVANTAGE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client | None = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Trade(BaseModel):
    symbol: str
    quantity: int
    price: float

def fetch_stock_price(symbol: str) -> float:
    if ALPHAVANTAGE_KEY:
        url = (
            f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHAVANTAGE_KEY}"
        )
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            raise HTTPException(status_code=400, detail="Error fetching data")
        data = r.json()
        try:
            return float(data["Global Quote"]["05. price"])
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid data received")
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1d")
    if hist.empty:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return hist["Close"][0]

@app.get("/stock/{symbol}")
def get_stock(symbol: str):
    price = fetch_stock_price(symbol)
    return {"symbol": symbol, "price": price}

@app.post("/trade")
def place_trade(trade: Trade, authorization: str | None = Header(None)):
    if supabase and authorization:
        token = authorization.replace("Bearer ", "")
        try:
            supabase.auth.get_user(token)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")
    return {"status": "success", "trade": trade}

