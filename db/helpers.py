import psycopg2
import psycopg2.extras
import db.config as config


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
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(sql_stmt)
    rows = None
    stmt_type = sql_stmt_type(sql_stmt)

    if stmt_type == 'SELECT':
        rows = cursor.fetchall()

    cursor.close()
    connection.commit()
    connection.close()

    return rows

def existing_symbols():
    """returns a list of existing symbols in the database."""
    rows = run_sql("SELECT * FROM stock")
    symbols = [row['symbol'] for row in rows]
    return rows

def insert_into_stock_table(symbol: str, name: str, exchange: str, shortable: bool):
    """inserts a record into the stock table"""
    name = name.replace("'", "''")
    try:
        run_sql(f"""INSERT INTO stock (symbol, name, exchange, shortable) 
                    VALUES ('{symbol}','{name}','{exchange}','{shortable}')""")
        print(f"Inserted record for {symbol}.")
    except Exception as e:
        print(e)