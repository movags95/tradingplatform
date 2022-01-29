from functions.db.helpers import run_sql, existing_symbols, symbol_to

def get_data_for_page(stock_id=None, strategy_id=None):
    """returns all data for stocks in db to display in jinja2 template. stocks, prices, strategies"""
    stocks = []
    prices = []
    strategies = []

    if stock_id:
        stocks = run_sql(f"""
            SELECT * FROM stock s
            WHERE id = {stock_id}
        """)
        prices = run_sql(f"""
            SELECT date::date, open, high, low, close, volume FROM stock_price_daily
            WHERE stock_id = {stock_id}
            ORDER BY date desc
        """)
        strategies = run_sql(f"""
            SELECT str.id, str.name, str.description, str.run_frequency FROM strategy str
            JOIN stock_strategy ss ON ss.strategy_id = str.id
            JOIN stock s on s.id = ss.stock_id
            WHERE ss.stock_id = {stock_id}
        """)
    
    elif strategy_id:
        stocks = run_sql(f"""
            SELECT s.id, s.symbol, s.name FROM strategy str
            JOIN stock_strategy ss ON ss.strategy_id = str.id
            JOIN stock s on s.id = ss.stock_id
            WHERE str.id = {strategy_id}
        """)
        prices = []
        strategies = run_sql(f"""
            SELECT * FROM strategy
            WHERE id = {strategy_id}
        """)

    else:
        stocks = run_sql(f"""
            SELECT * FROM stock
        """)
        prices = run_sql(f"""
            SELECT date::date, open, high, low, close, volume FROM stock_price_daily
            ORDER BY date desc
        """)
        strategies = run_sql(f"""
            SELECT * FROM strategy
        """)

    return stocks, prices, strategies
