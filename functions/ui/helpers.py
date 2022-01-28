from os import PRIO_USER
from functions.db.helpers import run_sql, existing_symbols, symbol_to
def get_data_for_stocks_layout():
    """returns all data for stocks in db to display in jinja2 template."""
    rows = run_sql("""
        SELECT * FROM stock ORDER BY symbol desc
    """)

    return rows
