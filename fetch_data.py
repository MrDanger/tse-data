from pytse_client.ticker import Ticker
import sys
import pandas as pd
import gspread
from jdatetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

symbol_name = sys.argv[1].replace('_', ' ')
sheet_name = os.environ.get('SHEET_NAME', default='temp')
hour = datetime.now().strftime('%H:%M:%S')
date = datetime.now().strftime('%Y-%m-%d')
credential = 'credentials.json'

try:
    # st_time = time.time()
    try:
        ticker = Ticker(symbol_name)
    except ValueError:
        from static import stock_names
        index = stock_names.get(symbol_name)
        ticker = Ticker("", index=index)

    real_time_data = ticker.get_ticker_real_time_info_response()
    total_buyers = 0
    total_sellers = 0
    total_buyers_vol = 0
    total_sellers_vol = 0
    for order in real_time_data.buy_orders:
        total_buyers_vol += order.volume
        total_buyers += order.count
    for order in real_time_data.sell_orders:
        total_sellers_vol += order.volume
        total_sellers += order.price

    gc = gspread.service_account(filename=credential)
    sh = gc.open(sheet_name)
    worksheet = sh.worksheet(symbol_name + ' 1')

    new_data = [
        {'symbol': symbol_name, 'data': date, 'hour': hour, 'NAV price': ticker.nav,
         'last trade price': real_time_data.last_price, 'deals count': real_time_data.count,
         'deals volume': real_time_data.volume, 'final price': real_time_data.adj_close,
         'total buyers count': total_buyers, 'total buyers volume': total_buyers_vol,
         'total sellers count': total_sellers, 'total sellers volume': total_sellers_vol,
         'individual buy volume': real_time_data.individual_trade_summary.buy_vol,
         'individual buy count': real_time_data.individual_trade_summary.buy_count,
         'individual sell volume': real_time_data.individual_trade_summary.sell_vol,
         'individual sell count': real_time_data.individual_trade_summary.sell_count,
         'corporate buy volume': real_time_data.corporate_trade_summary.buy_vol,
         'corporate buy count': real_time_data.corporate_trade_summary.buy_count,
         'corporate sell volume': real_time_data.corporate_trade_summary.sell_vol,
         'corporate sell count': real_time_data.corporate_trade_summary.sell_count, }]
    df = pd.DataFrame(new_data)
    if not worksheet.get_all_records():
        worksheet.append_rows([df.columns.tolist()] + df.values.tolist())
    else:
        worksheet.append_rows(df.values.tolist())
    # print(f'total time: {time.time() - st_time}')

except Exception as e:
    print(e)
