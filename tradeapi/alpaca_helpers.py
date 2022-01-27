import alpaca_trade_api as tradeapi
import tradeapi.config as config
import db.helpers as dbhelpers

def connect_api():
    try:
        api = tradeapi.REST(config.ALPACA_API_KEY, config.ALPACA_API_SECRET_KEY, config.ALPACA_BASE_URL)
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

def populate_stocks():
    assets = list_assets()
    existing_symbols = dbhelpers.existing_symbols()
    print("Populating stocks from API.")
    for asset in assets:
        try:
            if asset.status == "active" and asset.tradable is True and asset.symbol not in existing_symbols:
                dbhelpers.insert_into_stock_table(asset.symbol, asset.name, asset.exchange, asset.shortable)
        except Exception as e:
            print(e) 
    print("Population complete.")