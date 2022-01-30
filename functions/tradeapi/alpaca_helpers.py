from ctypes import util
import functions.tradeapi.alpaca_config as config
import functions.timezn.tzhelpers as timehelpers
import functions.db.helpers as dbhelpers
import alpaca_trade_api as tradeapi
from datetime import date, timedelta, datetime
import functions.utility


def connect_api(url=config.ALPACA_BASE_URL):
    try:
        api = tradeapi.REST(config.ALPACA_API_KEY,
                            config.ALPACA_API_SECRET_KEY,url)
        print("API connection successful.")
    except Exception as e:
        print(e)

    return api


def list_assets():
    try:
        api = connect_api()
        assets = api.list_assets()
    except Exception as e:
        print(e)

    return assets


def get_barset(symbols, start, end=date.today(), timeframe='1Day', limit=50):
    api = tradeapi.REST(config.ALPACA_API_KEY,config.ALPACA_API_SECRET_KEY)
    barset = api.get_bars(symbol=symbols, timeframe=timeframe,start=start, end=end, limit=limit)
    return barset
    


def populate_stocks():
    assets = list_assets()
    existing_symbols = dbhelpers.get_existing_symbols()
    print("Populating stocks from API.")
    for asset in assets:
        try:
            if asset.status == "active" and asset.tradable is True and asset.symbol not in existing_symbols:
                dbhelpers.insert_into_stock_table(
                    asset.symbol, asset.name, asset.exchange, asset.shortable)
        except Exception as e:
            print(e)
    print("Population complete.")


def populate_stock_price_daily(
    symbols=dbhelpers.get_existing_symbols(),
    Until=date.today(),
    From=date.today() - timedelta(1),
):
    """
    Function that populates the stock_price_daily table from alpaca.
    Inputs:
    - a list of symbols. By default will use all symbols in the db.
    - from/until is optional: date (default to todays date 1 days worth)
    """
    api = connect_api()
    chunk_size = config.ALPACA_REQUEST_LIMIT
    dtstart = timehelpers.to_alpaca_timestamp_format(From)
    dtend = timehelpers.to_alpaca_timestamp_format(Until)

    try:
        for i in range(0, len(symbols), chunk_size):
            symbol_chunk = symbols[i:i+chunk_size]
            barsets = api.get_barset(
                symbol_chunk, 'day', limit=1000, 
                start=dtstart, end=dtend
                )
            for symbol in barsets:
                dates = dbhelpers.get_dates_for_symbol(symbol)
                stock_id = dbhelpers.symbol_to(symbol)[1]
                for bar in barsets[symbol]:
                    if bar.t.date() not in dates:
                        print(f'Inserting record for {symbol}: {bar.t.date()}...')
                        dbhelpers.insert_into_stock_price_daily_table(
                            stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v
                        )
                    else:
                        print(f'Date {bar.t.date()} exists for {symbol}. Skipping...')
    

    except Exception as e:
        print(e)

def get_ohlc_snapshot_to_csv():
    api = connect_api()
    symbols = functions.utility.companies_csv_to_symbols_list()
    for symbol in symbols:
        barset = api.get_bars(symbol=[symbol], timeframe='1Day',start=date.today()-timedelta(100), end=date.today()-timedelta(1)).df
        barset.to_csv(f'data/daily/{symbol}.csv')
                
