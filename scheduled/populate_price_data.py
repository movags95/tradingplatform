import os,sys
sys.path.append(os.getcwd())

import functions
symbols = functions.db.helpers.existing_symbols('NYSE')
functions.alpaca_helpers.populate_stock_price_daily(symbols)