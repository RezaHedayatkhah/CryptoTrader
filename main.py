import talib
import numpy as np
from binance.client import Client
import time
from tradingview_ta import TA_Handler, Interval, Exchange
tesla = TA_Handler(
    symbol="TSLA",
    screener="america",
    exchange="NASDAQ",
    interval=Interval.INTERVAL_1_MINUTE
)

api_key = ''
api_secret = ''

client = Client(api_key, api_secret, testnet=True)

symbol = 'BTCUSDT'
quantity = 0.001

def get_indicators(symbol):
    candles = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE)
    print(candles)
    closes = np.array([float(candle[4]) for candle in candles])
    rsi = talib.RSI(closes, timeperiod=14)
    adx = talib.ADX(closes, closes, closes, timeperiod=14)
    upper, middle, lower = talib.BBANDS(closes, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    return rsi[-1], adx[-1], closes[-1], upper[-1], middle[-1], lower[-1]

def place_order(symbol, side, quantity):
    try:
        order = client.create_order(symbol=symbol, side=side, type=Client.ORDER_TYPE_MARKET, quantity=quantity)
        print(order)
    except Exception as e:
        print(e)

while True:
    try:
        rsi, adx, close, upper, middle, lower = get_indicators(symbol)
        print("rsi:", rsi)
        print("adx:", adx)
        print("close:", close)
        print("upper:", upper)
        print("middle:", middle)
        print("lower:", lower)
        if rsi < 30 and adx > 25 and close < lower:
            print('Placing buy order')
            place_order(symbol, Client.SIDE_BUY, quantity)
        elif rsi > 70 and adx > 25 and close > upper:
            print('Placing sell order')
            place_order(symbol, Client.SIDE_SELL, quantity)
    except Exception as e:
        print(e)

    time.sleep(60)