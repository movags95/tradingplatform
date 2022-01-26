import alpaca_trade_api
import config

def connect_api():
    try:
        api = alpaca_trade_api.REST(config.ALPACA_API_KEY, config.ALPACA_API_SECRET_KEY, config.ALPACA_BASE_URL)
    except Exception as e:
        print(e)

    return api