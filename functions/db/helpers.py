import psycopg2
import psycopg2.extras
import functions.db.config as config
from functions.utility import append_value_to_key


def connect_pgdb(hostname="localhost", db_name="tradingplatform", username="postgres", passwd="postgres", port=5555):
    """connects to the postgresdb and returns a connection."""
    try:
        conn = psycopg2.connect(
            host=config.HOSTNAME,
            database=config.DB_NAME,
            user=config.USERNAME,
            password=config.PASSWORD,
            port=config.PORT
        )
    except psycopg2.DatabaseError as e:
        print(e)

    return conn


def sql_stmt_type(sql_stmt):
    """determines the type of a sql statement. returns a string."""
    sql_type = None
    sql = sql_stmt.upper()
    if 'INSERT' in sql:
        sql_type = 'INSERT'
    elif 'UPDATE' in sql:
        sql_type = 'UPDATE'
    elif 'DELETE' in sql:
        sql_type = 'DELETE'
    elif 'SELECT' in sql:
        sql_type = 'SELECT'
    else:
        sql_type = None

    return sql_type

def run_sql(sql_stmt):
    """Creates a connection and executes a sql statement. Returns a set of rows or none if its an insert update or delete."""
    connection = connect_pgdb()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(sql_stmt)
    rows = None
    stmt_type = sql_stmt_type(sql_stmt)

    if stmt_type == 'SELECT':
        rows = cursor.fetchall()

    cursor.close()
    connection.commit()
    connection.close()

    return rows

def get_existing_symbols(exchange=None):
    """returns a list of existing symbols in the database."""
    if exchange:
        rows = run_sql(f"SELECT * FROM stock WHERE exchange = '{exchange}'")
    else: 
        rows = run_sql(f"SELECT * FROM stock")

    symbols = [row['symbol'] for row in rows]
    return symbols

def insert_into_stock_table(symbol: str, name: str, exchange: str, shortable: bool):
    """inserts a record into the stock table"""
    name = name.replace("'", "''")
    try:
        run_sql(f"""INSERT INTO stock (symbol, name, exchange, shortable) 
                    VALUES ('{symbol}','{name}','{exchange}','{shortable}')""")
        print(f"Inserted record for {symbol}.")
    except Exception as e:
        print(e)

def insert_into_stock_price_daily_table(stock_id, date, open, high, low, close, volume):
    """inserts a record into the stock_price_daily table"""
    try:
        run_sql(f"""INSERT INTO stock_price_daily (stock_id, date, open, high, low, close, volume) 
                    VALUES ({stock_id},'{date}',{open},{high},{low},{close},{volume})""")
    except Exception as e:
        print(e)

def insert_into_stock_strategy_table(stock_id: int, strategy_id: int):
    """inserts a record into the strategy table"""
    try:
        run_sql(f"""
            INSERT INTO stock_strategy (stock_id, strategy_id)
            VALUES ({stock_id}, {strategy_id})
        """)
    except Exception as e:
        print(e)

def delete_from_stock_strategy_table(strategy_id, stock_id):
    """Deletes a record from stock strategy table"""
    try:
        run_sql(f"""
            DELETE FROM stock_strategy WHERE strategy_id = {strategy_id} and stock_id = {stock_id}
        """)
    except Exception as e:
        print(e)

def delete_from_stock_watchlist_table(watchlist_id, stock_id):
    """Deletes a record into the stockwatchlist table"""
    try:
        run_sql(f"""
            DELETE FROM stock_watchlist WHERE watchlist_id = {watchlist_id} and stock_id = {stock_id}
        """)
    except Exception as e:
        print(e)

def insert_into_watchlist_table(name):
    """inserts a record into the watchlist table"""
    try:
        run_sql(f"""
            INSERT INTO watchlist (name)
            VALUES ('{name}')
        """)
    except Exception as e:
        print(e)

def delete_from_watchlist_table(watchlist_id):
    """Deletes a record into the watchlist table"""
    try:
        run_sql(f"""
            DELETE FROM watchlist WHERE id = {watchlist_id}
        """)
    except Exception as e:
        print(e)

def insert_into_stock_watchlist_table(watchlist_id, stock_id):
    """inserts a record into the stockwatchlist table"""
    try:
        run_sql(f"""
            INSERT INTO stock_watchlist (watchlist_id, stock_id)
            VALUES ({watchlist_id},{stock_id})
        """)
    except Exception as e:
        print(e)

def delete_from_stock_watchlist_table(watchlist_id, stock_id):
    """Deletes a record into the stockwatchlist table"""
    try:
        run_sql(f"""
            DELETE FROM stock_watchlist WHERE watchlist_id = {watchlist_id} and stock_id = {stock_id}
        """)
    except Exception as e:
        print(e)



def symbol_to(symbol, _max_date=False, _id=True):
    """
    Rerturns DB stock info on a given symbol.
    Format 0.dbsymbol, 1.sid, 2.name, 3.exchange, 4.shortable, 5.max_date
    """
    dbsymbol = None
    sid = None
    max_date = None
    name = None
    shortable = None
    exchange = None
    if _max_date:
        try:
            rows = run_sql(f"""
                        SELECT s.id as id, symbol, exchange, max(date) as date,
                        s.name as name, shortable
                        FROM stock s 
                        JOIN stock_price_daily spd on s.id = spd.stock_id
                        WHERE symbol ='{symbol}'
                        GROUP BY s.id
                        """)
            for row in rows:
                sid = row['id']
                max_date = row['date']
                dbsymbol = row['symbol']
                name = row['name']
                shortable = row['shortable']
                exchange = row['exchange']
        except Exception as e:
            print(e)
    elif _id:
        try:
            rows = run_sql(f"""SELECT id, symbol, name, exchange, shortable FROM stock
                                WHERE symbol = '{symbol}'""")
            for row in rows:
                sid = row['id']
                max_date = None
                dbsymbol = row['symbol']
                name = row['name']
                shortable = row['shortable']
                exchange = row['exchange']
        except Exception as e:
            print(e)

    return dbsymbol, sid, name, exchange, shortable, max_date

def get_dates_for_symbol(symbol):
    dates = []
    try:
        rows = run_sql(f"""
        SELECT distinct date 
        FROM stock_price_daily spd 
        JOIN stock s on s.id = spd.stock_id 
        WHERE symbol = '{symbol}'"""
        )
        for row in rows:
            dates.append(row['date'].date())
    except Exception as e:
        print(e)

    return dates

def get_watchlists_dict():
    data = run_sql('SELECT * FROM watchlist')
    watchlist_dict = {}
    if data:
        for watchlist in data:
            watchlist_dict[watchlist[0]] = watchlist[1]
    
    return watchlist_dict

def get_stock_watctchlist_dict():
    data = run_sql("""
        SELECT * FROM stock_watchlist ORDER BY watchlist_id
    """)
    
    stock_watchlist_dict = {}
    for stock_watchlist in data:
        append_value_to_key(stock_watchlist_dict, stock_watchlist[0], stock_watchlist[1])

    return stock_watchlist_dict



    