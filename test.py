import tradeapi.alpaca_helpers as apihelper
import tradeapi.config as config

api = apihelper.connect_api()
print(api)