from tracemalloc import start
from aiohttp import request
from functions.db.helpers import connect_pgdb, delete_from_stock_watchlist_table, insert_into_stock_price_daily_table, insert_into_stock_table, get_existing_symbols, run_sql, symbol_to, get_dates_for_symbol, insert_into_stock_strategy_table, get_watchlists_dict, get_stock_watctchlist_dict, delete_from_watchlist_table
from functions.timezn.tzhelpers import to_date, to_alpaca_timestamp_format
from functions.tradeapi.alpaca_helpers import connect_api, get_barset, list_assets, populate_stocks, populate_stock_price_daily
from functions.ui.helpers import get_data_for_page
from functions.db.create_db import create_indexes, create_tables, drop_schema, drop_tables, insert_strategies
import requests
import functions.tradeapi.alpaca_config as config
import json,os
import pandas as pd
from datetime import date, timedelta
from alpaca_trade_api import REST
import talib
from functions.utility import append_value_to_key

datafiles = os.listdir('data/daily')
for filename in datafiles:
    df = pd.read_csv(f'data/daily/{filename}', encoding='unicode_escape')
    print(df)
   

# delete_from_watchlist_table(10)
# from functions.utility import watchlist_to_dict

# selected_watchlist_id = 1
# dict = get_stock_watctchlist_dict()
# for item in dict:
#     if item == selected_watchlist_id:
#         print(dict[item])


# watchlists = get_watchlists_dict()
# for item in watchlists:
#     print(watchlists[item])

# print(watchlists)

# morning_stars = talib.CDLMORNINGSTAR(barset['open'], barset['high'], barset['low'], barset['close'])
# engulfing = talib.CDLENGULFING(barset['open'], barset['high'], barset['low'], barset['close'])
# barset['Morning Star'] = morning_stars
# barset['Engulfing'] = engulfing

# engulfing_days = barset[barset['Engulfing'] != 0 ]
# print(engulfing_days)

# # params = '?timeframe=1Day&start=2021-10-01&end=2022-01-01'
# # url = config.BARS_URL.format('AAPL,MSFT') + params
# api = connect_api(config.BARS_URL)
# bars = api.get_bars('AAPL','1Day')
# bars = bars._raw
# print(bars)





# url = config.BARS_URL.format('MSFT')
# params = {
#     'start':'2021-08-01',
#     'end':'2022-01-01',
#     'timeframe':'1Day'
# }
# r = requests.get(url=url, params=params, headers=config.HEADERS)
# print(url)
# print(r.content)