from binance.client import Client
import time

api_key = ''
api_secret = ''

client = Client(api_key, api_secret, testnet=True)

balance = client.get_asset_balance(asset='BTC')
print(balance)

symbol = 'BTCUSDT'
candles = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE)
print(candles)