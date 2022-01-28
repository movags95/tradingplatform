import os,sys
sys.path.append(os.getcwd())

import functions

def main(exchange):
    symbols = functions.db.helpers.existing_symbols(exchange)
    functions.alpaca_helpers.populate_stock_price_daily(symbols)

if __name__ == '__main__':
    main('NASDAQ')