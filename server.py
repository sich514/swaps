from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import threading
import time

app = FastAPI()

# Разрешаем CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEX_SCREENER_API_URL = "https://api.dexscreener.io/latest/dex/trades"
NETWORKS = ["solana", "ethereum", "base"]  # Сети
THRESHOLD = 10000  # Порог суммы сделки

# Хранилище для данных о больших сделках
big_trades = []

def monitor_trades():
    global big_trades
    while True:
        temp_trades = []
        for network in NETWORKS:
            try:
                response = requests.get(f"{DEX_SCREENER_API_URL}?network={network}")
                trades = response.json().get("trades", [])
                
                for trade in trades:
                    if trade["amountUSD"] > THRESHOLD:
                        temp_trades.append(trade)
            except Exception as e:
                print(f"Error fetching trades for {network}: {e}")
        big_trades = temp_trades
        time.sleep(10)  # Обновляем каждые 10 секунд

# Запускаем мониторинг в отдельном потоке
thread = threading.Thread(target=monitor_trades, daemon=True)
thread.start()

@app.get("/big-trades/")
def get_big_trades():
    return big_trades
