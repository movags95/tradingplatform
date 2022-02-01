import functions.tradeapi.alpaca_helpers as apihelpers
import os,sys
sys.path.append(os.getcwd())

import functions

def main():
    apihelpers.get_ohlc_snapshot_to_csv()

if __name__ == '__main__':
    main()
