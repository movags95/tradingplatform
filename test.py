import tradeapi.alpaca_helpers as apihelper
import db.helpers as dbhelper

apihelper.populate_stocks()

# assets = apihelper.list_assets()
# exchanges = []
# symbols = []
# for asset in assets:
#     if asset.exchange not in exchanges:
#         exchanges.append(asset.exchange)
#     if asset.exchange == 'AMEX':
#         symbols.append(asset.symbol)
# print(exchanges)
# # print(symbols)

# print(dbhelper.insert_into_stock_table('AAPL',"hello's","sexy",True))



