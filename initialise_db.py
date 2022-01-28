from functions.db import drop_tables, create_tables, insert_strategies
from functions.tradeapi import populate_stocks

try:
    drop_tables()
except Exception as e:
    print("Could not drop tables. They might not be created.")
    pass

create_tables()
insert_strategies()
populate_stocks()
