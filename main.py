import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from functions.db.helpers import run_sql, insert_into_stock_strategy_table
from functions.tradeapi.alpaca_helpers import get_ohlc_snapshot_to_csv
from functions.ui.helpers import get_data_for_page
import data.talib_indicators as talib_indicators

import pandas as pd
import talib



app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/") #function for the root page
def stocks(request: Request):
    html = "page_stocks.html"
    data = run_sql("""
        SELECT s.id, symbol, name, exchange, shortable, close FROM stock s
        JOIN stock_price_daily spd
        ON s.id = spd.stock_id
        AND spd.date = (select max(date) as date from stock_price_daily)
        ORDER BY exchange desc, symbol
    """)
    headings = ['','ID', 'Symbol', 'Name', 'Exchange', 'Shortable', 'Last Close']

    return templates.TemplateResponse(html, {'request': request, 'headings': headings, 'data':data})


@app.get('/stock/{stock_id}')
def stock_detail(request: Request, stock_id):
    html = "page_stock_detail.html"
    stocks, prices, strategies= get_data_for_page(page=html, stock_id=stock_id)
    strategies = run_sql('SELECT * FROM strategy')
    headings = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

    return templates.TemplateResponse(html, {
        'request': request,
        'headings': headings, 
        'data': prices, 
        'stocks': stocks, 
        'strategies': strategies
        })


@app.get('/strategies')
def strategies(request: Request):
    html = "page_strategies.html"
    strategies = get_data_for_page(page=html)[2]
    headings = ['', 'ID', 'Strategy', 'Description', 'Run Frequency']

    return templates.TemplateResponse(html, {
        'request': request,
        'headings': headings, 
        'data': strategies
        })


@app.get('/strategy/{strategy_id}')
def strategies(request: Request, strategy_id):
    html = "page_strategy_detail.html"
    stocks, prices, strategies= get_data_for_page(page=html, strategy_id=strategy_id)
    headings = ['ID', 'Symbol', 'Name']

    return templates.TemplateResponse(html, {
        'request': request,
        'headings': headings, 
        'data': stocks,
        'strategy': strategies
        })


@app.post("/apply-strategy")
def apply_strategy(strategy_id: int = Form(...), stock_id: int = Form(...)):
    insert_into_stock_strategy_table(stock_id, strategy_id)
    return RedirectResponse(url=f"/strategy/{strategy_id}", status_code=303)


@app.get('/candlesticks')
def candlestick_screener(request: Request):
    html = "page_candlesticks.html"
    pattern = request.query_params.get('pattern', None)
    if pattern:
        datafiles = os.listdir('data/daily')
        for filename in datafiles:
            df = pd.read_csv(f'data/daily/{filename}')
            function4pattern = getattr(talib, pattern)
            symbol = filename.split('.')[0]
            print(symbol)
            try:
                result = function4pattern(df['open'], df['high'], df['low'], df['close'])
                last = result.tail(1).values[0]
                if last > 0:
                    pass
                elif last < 0:
                    pass

            except Exception as e:
                print(f'Unable to produce results for {filename}')


    return templates.TemplateResponse(html, {
        'request': request,
        'patterns': talib_indicators.candlestick_functions
        })

@app.get('/snapshot')
def snapshot(request: Request):
    get_ohlc_snapshot_to_csv()


# @app.post('/orders')
# def orders(request: Request):
#     html="page_orders.html"
#     pass