from pytse_client.ticker import Ticker
import sys
from datetime import datetime
import pandas as pd
import gspread
import time

symbol_name = sys.argv[1]
hour = datetime.now().strftime('%H:%M:%S')
date = datetime.now().strftime('%Y-%m-%d')
credential = 'credentials.json'

try:
    # st_time = time.time()
    ticker = Ticker(symbol_name)
    message = f'symbol name: {symbol_name}\n' \
              f'date: {date}\n' \
              f'NAV price: {ticker.nav}\n'
    real_time_data = ticker.get_ticker_real_time_info_response()
    message += f'last trade price: {real_time_data.last_price}\n' \
               f'deals count: {real_time_data.count}\n' \
               f'deals volume: {real_time_data.volume}\n' \
               f'final price: {real_time_data.adj_close}\n'
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
    message += f'total buyers count: {total_buyers}\n' \
               f'total buyers volume: {total_buyers_vol}\n' \
               f'total sellers count: {total_sellers}\n' \
               f'total sellers volume: {total_sellers_vol}\n'
    real_data = ticker.client_types
    message += f'individual buy volume: {real_data.individual_buy_vol[0]}\n' \
               f'individual buy count: {real_data.individual_buy_count[0]}\n' \
               f'individual sell volume: {real_data.individual_sell_vol[0]}\n' \
               f'individual sell count: {real_data.individual_sell_count[0]}\n' \
               f'corporate buy volume: {real_data.corporate_buy_vol[0]}\n' \
               f'corporate buy count: {real_data.corporate_buy_count[0]}\n' \
               f'corporate sell volume: {real_data.corporate_sell_vol[0]}\n' \
               f'corporate sell count: {real_data.corporate_sell_count[0]}\n'
    # print(message)
    gc = gspread.service_account(filename=credential)
    sheet_name = symbol_name
    sh = gc.open(sheet_name)
    worksheet = sh.get_worksheet(0)
    new_data = [
        {'symbol': symbol_name, 'data': date, 'hour': hour, 'NAV price': ticker.nav,
         'last trade price': real_time_data.last_price, 'deals count': real_time_data.count,
         'deals volume': real_time_data.volume, 'final price': real_time_data.adj_close,
         'total buyers count': total_buyers, 'total buyers volume': total_buyers_vol,
         'total sellers count': total_sellers, 'total sellers volume': total_sellers_vol,
         'individual buy volume': real_data.individual_buy_vol[0],
         'individual buy count': real_data.individual_buy_count[0],
         'individual sell volume': real_data.individual_sell_vol[0],
         'individual sell count': real_data.individual_sell_count[0],
         'corporate buy volume': real_data.corporate_buy_vol[0],
         'corporate buy count': real_data.corporate_buy_count[0],
         'corporate sell volume': real_data.corporate_sell_vol[0],
         'corporate sell count': real_data.corporate_sell_count[0], }]
    df = pd.DataFrame(new_data)
    worksheet.append_rows(df.values.tolist())
    # print(f'total time: {time.time() - st_time}')

except EOFError as e:
    print(e)