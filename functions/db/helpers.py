import psycopg2
import psycopg2.extras
import functions.db.config as config


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

def existing_symbols(exchange=None):
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

# DECOMMISIONED
# def symbol_max_date(symbol):
#     """returns the max date that exists for a given symbol"""
#     sid = None
#     max_date = None
#     try:
#         rows = run_sql(f"""SELECT s.id as id, symbol, max(date) as date
#                     FROM stock_price_daily spd 
#                     JOIN stock s on s.id = spd.stock_id
#                     WHERE symbol ='{symbol}'
#                     GROUP BY s.id""")
#         for row in rows:
#             sid = row['id']
#             max_date = row['date']
#     except Exception as e:
#         print(e)

#     return sid, symbol, max_date

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

def get_symbol_dates(symbol):
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


    