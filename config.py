#Configure parameters before use

import os

env_var = os.environ.get('CONFIG_PY')
if env_var == 'docker':
    DB_PATH = '/app/app.db'
else:
    DB_PATH = '/Users/mohitvaghela/Documents/Hobby/GitRepos/tradingplatform/app.db'


STOCK_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY,     
        symbol TEXT NOT NULL UNIQUE, 
        name TEXT NOT NULL,
        exchange TEXT NOT NULL,
        shortable BOOLEAN NOT NULL
    )
"""

PRICE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS stock_price (
        id INTEGER PRIMARY KEY, 
        stock_id INTEGER,
        date NOT NULL,
        open NOT NULL, 
        high NOT NULL, 
        low NOT NULL, 
        close NOT NULL, 
        volume NOT NULL,
        sma_20,
        sma_50,
        rsi_14,
        FOREIGN KEY (stock_id) REFERENCES stock (id) ON DELETE CASCADE,
        UNIQUE (stock_id,date)
    )
"""

STRATEGY_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS strategy (
        id INTEGER PRIMARY KEY, 
        name NOT NULL,
        description,
        run_frequency
    )
"""

STOCK_STRAT_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS stock_strategy (
        stock_id INTEGER NOT NULL, 
        strategy_id INTEGER NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id) ON DELETE CASCADE,
        FOREIGN KEY (strategy_id) REFERENCES strategy (id) ON DELETE CASCADE,
        UNIQUE (stock_id, strategy_id)
    )
"""

STOCK_SELECT_SQL = """SELECT id, symbol, name, exchange, shortable FROM stock"""
PRICE_SELECT_SQL = """SELECT id, stock_id, date, open, high, low, close, volume, sma_20, sma_50, rsi_14 FROM stock_price"""
STRATEGY_SELECT_SQL = """SELECT id, name, description, run_frequency FROM strategy"""
STOCK_STRAT_SELECT_SQL = """SELECT stock_id,strategy_id FROM stock_strategy"""
INDICATORS_SELECT_SQL = """
        SELECT symbol, close, rsi_14, sma_20, sma_50, date 
        FROM stock s
        JOIN stock_price sp on s.id = sp.stock_id
        WHERE date = (select max(date) from stock_price)
    """
