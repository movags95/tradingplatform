from functions.db.helpers import run_sql, existing_symbols, symbol_to

def get_data_stock_daily_html(symbol):
    """returns all data for stocks in db to display in jinja2 template."""
    stocks = run_sql(f"""
        SELECT * FROM stock s
        WHERE symbol = '{symbol}'
    """)

    prices = run_sql(f"""
        SELECT * FROM stock s 
        JOIN stock_price_daily spd 
        ON s.id = spd.stock_id
        WHERE s.symbol = '{symbol}' 
        ORDER BY date desc
    """)

    stratagies = run_sql("""
        SELECT * FROM strategy 
    """)

    return stocks, prices, stratagies
