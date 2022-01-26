import tradeapi.alpaca_helpers as apihelper
import db.helpers as dbhelper

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

symbols = dbhelper.existing_symbols()

for symbol in symbols:
    print(symbol['symbol'])

dbhelper.insert_into_stock_table('AMC',"AMC Entertainment",'NYSE',True)