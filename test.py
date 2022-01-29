from functions.db.helpers import insert_into_stock_price_daily_table, insert_into_stock_table, get_existing_symbols, symbol_to, get_dates_for_symbol, insert_into_stock_strategy_table
from functions.timezn.tzhelpers import to_date, to_alpaca_timestamp_format
from functions.tradeapi.alpaca_helpers import connect_api, list_assets, populate_stocks, populate_stock_price_daily
from functions.ui.helpers import get_data_for_page
from functions.db.create_db import create_indexes, create_tables, drop_schema, drop_tables, insert_strategies

create_indexes()
# populate_stock_price_daily(['AAPL','MSFT'])
# from time import strptime
# import tradeapi.alpaca_helpers as apihelpers
# import db.helpers as dbhelpers
# import timezn.helpers as timehelpers
# from datetime import date, datetime
# print(dbhelpers.symbol_max_date('AAPL'))
# print(dbhelpers.symbol_max_date('AAPL')[2])
# high = datetime.strptime("2022-01-16","%Y-%m-%d")
# low = datetime.strptime("2022-01-03","%Y-%m-%d")
# print(low>high)
# print(date.today())
# print(timehelper.to_alpaca_timestamp_format('11-JAN-2020T12:24'))
# apihelpers.populate_stock_price_daily(['AAPL','MSFT'])

# print(dbhelpers.symbol_to('AAPL'))

# print(dbhelper.symbol_max_date('AAPL'))

# apihelper.populate_stocks()

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




