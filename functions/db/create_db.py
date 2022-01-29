import functions.db.helpers as helpers

def drop_schema():
    helpers.run_sql("DROP SCHEMA public CASCADE")
    helpers.run_sql("CREATE SCHEMA public")
    print("Dropped and recreated SCHEMA public.")

def drop_tables():
    helpers.run_sql("DROP TABLE stock CASCADE")
    helpers.run_sql("DROP TABLE stock_price_daily CASCADE")
    helpers.run_sql("DROP TABLE strategy CASCADE")
    helpers.run_sql("DROP TABLE stock_strategy CASCADE")
    print("Dropped all tables.")

def create_tables():
    helpers.run_sql("""
        CREATE TABLE IF NOT EXISTS stock (
            id SERIAL PRIMARY KEY,     
            symbol TEXT NOT NULL UNIQUE, 
            name TEXT NOT NULL,
            exchange TEXT NOT NULL,
            shortable BOOLEAN NOT NULL
        )
    """)
    print("Stock table created")

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
            FOREIGN KEY (stock_id) REFERENCES stock (id) ON DELETE CASCADE,
            UNIQUE (stock_id,date)
        )
    """)
    print("Stock price daily table created.")

    helpers.run_sql("""
        CREATE TABLE IF NOT EXISTS strategy (
            id SERIAL PRIMARY KEY, 
            name TEXT NOT NULL,
            description TEXT,
            run_frequency TEXT
        )
    """)
    print("Strategy table created.")

    helpers.run_sql("""
        CREATE TABLE IF NOT EXISTS stock_strategy (
            stock_id SERIAL NOT NULL, 
            strategy_id INTEGER NOT NULL,
            FOREIGN KEY (stock_id) REFERENCES stock (id) ON DELETE CASCADE,
            FOREIGN KEY (strategy_id) REFERENCES strategy (id) ON DELETE CASCADE,
            UNIQUE (stock_id, strategy_id)
        )
    """)
    print("Stock strategy table created.")

def insert_strategies():
    helpers.run_sql("""
    insert into strategy (name, description, run_frequency) 
    values ('opening_range_breakout', 'A strategy that looks for the high and low in the first 15 mins to calculate a range, which is used to enter a long trade.','1 min')
    """)

    helpers.run_sql("""
    insert into strategy (name, description, run_frequency) 
    values ('opening_range_breakdown', 'A strategy that looks for the high and low in the first 15 mins to calculate a range, which is used to enter a short trade.','1 min')
    """)

    helpers.run_sql("""
    insert into strategy (name, description, run_frequency) 
    values ('bollinger_bands', 'A strategy that looks detects when a candle closes out of the bollinger band and will long or short based on the next candle closing within the band.','1 day')
    """)

    print("Strategies inserted into strategy table.")

def create_indexes():
    helpers.run_sql('CREATE INDEX IF NOT EXISTS idx_spd_sid ON stock_price_daily(stock_id)')
    helpers.run_sql('CREATE INDEX IF NOT EXISTS idx_spd_date ON stock_price_daily(date)')
    print('Indexes created.')
