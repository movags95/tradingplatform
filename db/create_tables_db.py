import helpers as helpers

helpers.run_sql("DROP SCHEMA public CASCADE")
helpers.run_sql("CREATE SCHEMA public")

helpers.run_sql("""
    CREATE TABLE IF NOT EXISTS stock (
        id SERIAL PRIMARY KEY,     
        symbol TEXT NOT NULL UNIQUE, 
        name TEXT NOT NULL,
        exchange TEXT NOT NULL,
        shortable BOOLEAN NOT NULL
    )
""")

helpers.run_sql("""
    CREATE TABLE IF NOT EXISTS stock_price_daily (
        id SERIAL PRIMARY KEY, 
        stock_id INTEGER,
        date TIMESTAMP NOT NULL,
        open NUMERIC NOT NULL, 
        high NUMERIC NOT NULL, 
        low NUMERIC NOT NULL, 
        close NUMERIC NOT NULL, 
        volume NUMERIC NOT NULL,
        sma_20 NUMERIC,
        sma_50 NUMERIC,
        rsi_14 NUMERIC,
        FOREIGN KEY (stock_id) REFERENCES stock (id) ON DELETE CASCADE,
        UNIQUE (stock_id,date)
    )
""")

helpers.run_sql("""
    CREATE TABLE IF NOT EXISTS strategy (
        id SERIAL PRIMARY KEY, 
        name TEXT NOT NULL,
        description TEXT,
        run_frequency TEXT
    )
""")

helpers.run_sql("""
    CREATE TABLE IF NOT EXISTS stock_strategy (
        stock_id SERIAL NOT NULL, 
        strategy_id INTEGER NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id) ON DELETE CASCADE,
        FOREIGN KEY (strategy_id) REFERENCES strategy (id) ON DELETE CASCADE,
        UNIQUE (stock_id, strategy_id)
    )
""")

