import os,sys

sys.path.append(os.getcwd()+'/functions')
print(sys.path)

import functions

functions.alpaca_helpers.populate_stock_price_daily()