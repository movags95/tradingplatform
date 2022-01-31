from tracemalloc import start
from aiohttp import request
from functions.db.helpers import insert_into_stock_price_daily_table, insert_into_stock_table, get_existing_symbols, symbol_to, get_dates_for_symbol, insert_into_stock_strategy_table
from functions.timezn.tzhelpers import to_date, to_alpaca_timestamp_format
from functions.tradeapi.alpaca_helpers import connect_api, get_barset, list_assets, populate_stocks, populate_stock_price_daily
from functions.ui.helpers import get_data_for_page
from functions.db.create_db import create_indexes, create_tables, drop_schema, drop_tables, insert_strategies
import requests
import functions.tradeapi.alpaca_config as config
import json
import pandas as pd
from datetime import date, timedelta
from alpaca_trade_api import REST
import talib

api = connect_api()
symbols = get_existing_symbols('AMEX')
# symbols = ["AAPL"]
for symbol in symbols:
    barset = api.get_bars(symbol=[symbol], timeframe='1Day',start=date.today()-timedelta(100), end=date.today()-timedelta(1)).df
    barset.to_csv(f'data/daily/{symbol}.csv')
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