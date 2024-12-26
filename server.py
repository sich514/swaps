from fastapi import FastAPI
import requests

app = FastAPI()

DEX_SCREENER_API_URL = "https://api.dexscreener.io/latest/dex/trades"

@app.get("/big-trades/")
def get_big_trades():
    networks = ["solana", "ethereum"]  # Сети
    threshold = 20000  # Пороговая сумма сделки
    big_trades = []

    for network in networks:
        response = requests.get(f"{DEX_SCREENER_API_URL}?network={network}")
        trades = response.json().get("trades", [])
        
        for trade in trades:
            if trade["amountUSD"] > threshold:
                big_trades.append(trade)
    
    return big_trades
