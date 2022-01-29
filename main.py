# from datetime import date, timedelta
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from functions.db.helpers import get_dates_for_symbol, run_sql, insert_into_stock_strategy_table
from functions.ui.helpers import get_data_for_page

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/") #function for the root page
def stocks(request: Request):
    
    data = run_sql("""
        SELECT s.id, symbol, name, exchange, shortable, close FROM stock s
        JOIN stock_price_daily spd
        ON s.id = spd.stock_id
        AND spd.date = (select max(date) as date from stock_price_daily)
        ORDER BY exchange desc, symbol
    """)

    headings = ['','ID', 'Symbol', 'Name', 'Exchange', 'Shortable', 'Last Close']

    return templates.TemplateResponse("page_stocks.html", {'request': request, 'headings': headings, 'data':data})


@app.get('/stock/{stock_id}')
def stock_detail(request: Request, stock_id):
    stocks, prices, strategies= get_data_for_page(stock_id=stock_id)
    strategies = run_sql('SELECT * FROM strategy')
    headings = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

    return templates.TemplateResponse("page_stock_detail.html", {
        'request': request,
        'headings': headings, 
        'data': prices, 
        'stocks': stocks, 
        'strategies': strategies
        })


@app.get('/strategies')
def strategies(request: Request):
    strategies = get_data_for_page()[2]
    headings = ['', 'ID', 'Strategy', 'Description', 'Run Frequency']

    return templates.TemplateResponse("page_strategies.html", {
        'request': request,
        'headings': headings, 
        'data': strategies
        })


@app.get('/strategy/{strategy_id}')
def strategies(request: Request, strategy_id):
    stocks, prices, strategies= get_data_for_page(strategy_id=strategy_id)
    headings = ['ID', 'Symbol', 'Name']

    return templates.TemplateResponse("page_strategy_detail.html", {
        'request': request,
        'headings': headings, 
        'data': stocks,
        'strategy': strategies
        })


@app.post("/apply-strategy")
def apply_strategy(strategy_id: int = Form(...), stock_id: int = Form(...)):
    insert_into_stock_strategy_table(stock_id, strategy_id)
    return RedirectResponse(url=f"/strategy/{strategy_id}", status_code=303)