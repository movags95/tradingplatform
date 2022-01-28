from datetime import datetime
import alpaca_trade_api as tradeapi
import pandas as pd
from datetime import date

def to_alpaca_timestamp_format(fromdate=date.today(), TZ='America/New_York'):
    """takes in date in the format of yyyy-mm-dd or 2020-11-04T07:00
        and converts it to alpacas date parm format. defaults to todays date 00:00
    """
    todate = pd.Timestamp(fromdate, tz=TZ).isoformat()
    return todate

def to_date(date, format="%Y-%m-%d"):
    if date:
        return datetime.strptime(date, format)
    else:
        print('Date not accepted in to_date func therefore not converted. Possible None value.')