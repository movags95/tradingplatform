import os,sys
sys.path.append(os.getcwd())

import functions

def main():
    functions.alpaca_helpers.populate_stocks()

if __name__ == '__main__':
    main()
