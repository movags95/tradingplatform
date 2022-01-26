import alpaca_trade_api as tradeapi
import tradeapi.config as config

def connect_api():
    try:
        api = tradeapi.REST(config.ALPACA_API_KEY, config.ALPACA_API_SECRET_KEY, config.ALPACA_BASE_URL)
    except Exception as e:
        print(e)

    return api