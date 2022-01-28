# from datetime import date, timedelta
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from functions.db.helpers import run_sql
from functions.ui.helpers import get_data_stock_daily_html



app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/") #function for the root page
def index(request: Request):
    
    stocks = run_sql("""
        SELECT * FROM stock s
        JOIN stock_price_daily spd
        ON s.id = spd.stock_id
        AND spd.date = (select max(date) as date from stock_price_daily)
        ORDER BY exchange desc, symbol
    """)

    return templates.TemplateResponse("index.html", {'request': request, 'stocks': stocks})

@app.get('/stock/{symbol}')
def stock_daily_detail(request: Request, symbol):
    
    stocks, prices, strategies = get_data_stock_daily_html(symbol)

    return templates.TemplateResponse("stock_daily_detail.html", {'request': request, 'stocks': stocks, "prices": prices, 'strategies': strategies})