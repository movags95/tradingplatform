from db.create_db import drop_tables,create_tables,insert_strategies
from tradeapi.alpaca_helpers import populate_stocks

drop_tables()
create_tables()
insert_strategies()
populate_stocks()
