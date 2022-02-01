import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from functions.db.helpers import delete_from_stock_watchlist_table, delete_from_watchlist_table, get_watchlists_dict, insert_into_stock_watchlist_table, run_sql, insert_into_stock_strategy_table, insert_into_watchlist_table, get_stock_watctchlist_dict, delete_from_watchlist_table
from functions.tradeapi.alpaca_helpers import get_ohlc_snapshot_to_csv
from functions.ui.helpers import get_data_for_page
from functions.utility import companies_csv_to_dict
import data.talib_indicators as talib_indicators

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
    headings = ['','ID', 'Symbol', 'Name', 'Exchange', 'Shortable', 'Last Close', 'Add to Watchlist']

    watchlists = get_watchlists_dict()
    selected_watchlist_id = request.query_params.get('selected_watchlist', None)
    stock_watchlist = get_stock_watctchlist_dict()


    return templates.TemplateResponse(html, 
    {'request': request,
     'headings': headings, 
     'data':data, 
     'watchlists':watchlists,
     'selected_watchlist_id':int(selected_watchlist_id) if selected_watchlist_id else None,
     'stock_watchlist': stock_watchlist
    })

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
    companies, symbols = companies_csv_to_dict()
    pattern = request.query_params.get('pattern', None)
    
    if pattern:
        datafiles = os.listdir('data/daily')
        for filename in datafiles:
            df = pd.read_csv(f'data/daily/{filename}')
            function4pattern = getattr(talib, pattern)
            symbol = filename.split('.')[0]
            try:
                result = function4pattern(df['open'], df['high'], df['low'], df['close'])
                last = result.tail(1).values[0]
                if last > 0:
                    companies[symbol][pattern] = 'bullish'
                elif last < 0:
                    companies[symbol][pattern] = 'bearish'
                else:
                    companies[symbol][pattern] = None

            except Exception as e:
                print(f'Unable to produce results for {filename}')


    return templates.TemplateResponse(html, {
        'request': request,
        'patterns': talib_indicators.candlestick_functions,
        'companies': companies,
        'selected_pattern': pattern
        })

@app.get('/watchlists')
def watchlists(request: Request):
    html = "page_watchlists.html"
    watchlists = get_data_for_page(page=html)
    headings = ['','ID', 'Name','Delete?']

    return templates.TemplateResponse(html, {
        'request': request,
        'headings': headings, 
        'data': watchlists
        })

@app.get('/watchlist/{watchlist_id}')
def watchlist_detail(request: Request, watchlist_id):
    html = "page_watchlist_detail.html"
    watchlist, stocks = get_data_for_page(page=html, watchlist_id=watchlist_id)
    headings = ['', 'ID', 'Symbol', 'Name', 'Exchange', 'Shortable', '']

    return templates.TemplateResponse(html, {
        'request': request,
        'headings': headings, 
        'data': stocks,
        'watchlist': watchlist
        })

# @app.get('/snapshot')
# def snapshot(request: Request):
#     get_ohlc_snapshot_to_csv()

@app.post("/create-watchlist")
def create_watchlist(new_watchlist_name: str = Form(...)):
    try:
        insert_into_watchlist_table(new_watchlist_name)
        print(f'Watchlist: {new_watchlist_name} created.')
    except:
        pass
    return RedirectResponse(url="/watchlists", status_code=303)

@app.get('/delete-watchlist/{watchlist_id}')
def delete_watchlist(request: Request, watchlist_id):
    print(watchlist_id)
    try:
        watchlist_id = int(watchlist_id)
        delete_from_watchlist_table(watchlist_id)
        print(f'Watchlist deleted.')
    except:
        pass
    return RedirectResponse(url="/watchlists", status_code=303)

@app.get('/add-to-watchlist/{watchlist_id}/{stock_id}')
def add_to_watchlist(request: Request, watchlist_id, stock_id):
    watchlist_dict = get_stock_watctchlist_dict()
    if watchlist_id and stock_id:
        insert_into_stock_watchlist_table(watchlist_id, stock_id)

    return RedirectResponse(url=f"/?selected_watchlist={watchlist_id}", status_code=303)

@app.get('/delete-from-watchlist/{watchlist_id}/{stock_id}')
def delete_from_watchlist(request: Request, watchlist_id, stock_id):
    watchlist_dict = get_stock_watctchlist_dict()
    if watchlist_id and stock_id and watchlist_dict[int(watchlist_id)]:
        delete_from_stock_watchlist_table(watchlist_id, stock_id)

    return RedirectResponse(url=f"/?selected_watchlist={watchlist_id}", status_code=303)

@app.get('/delete-from-watchlist-redirect-wl/{watchlist_id}/{stock_id}')
def delete_from_watchlist(request: Request, watchlist_id, stock_id):
    watchlist_dict = get_stock_watctchlist_dict()
    if watchlist_id and stock_id and watchlist_dict[int(watchlist_id)]:
        delete_from_stock_watchlist_table(watchlist_id, stock_id)

    return RedirectResponse(url=f"/watchlist/{watchlist_id}", status_code=303)

# @app.post('/orders')
# def orders(request: Request):
#     html="page_orders.html"
#     pass