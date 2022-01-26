import helpers as helpers

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