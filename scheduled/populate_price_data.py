import os,sys
sys.path.append(os.getcwd())

import functions

def main(exchange=None, symbol_list=None, start=None):
    if symbol_list is None:
        symbols = functions.db.helpers.get_existing_symbols(exchange)
    else:
        symbols = symbol_list
    if start is None:
        functions.alpaca_helpers.populate_stock_price_daily(symbols)
    else: 
        functions.alpaca_helpers.populate_stock_price_daily(symbols, From=start)

if __name__ == '__main__':
    # main(symbol_list=['AAPL'], start="2021-06-01")
    main(symbol_list=['AAPL','MSFT'], start="2022-01-01")