import sys
from datetime import datetime
import pandas as pd
import gspread

symbol_name = sys.argv[1]
count = int(sys.argv[2])

hour = datetime.now().strftime('%H:%M:%S')
date = datetime.now().strftime('%Y-%m-%d')
credential = 'credentials.json'

try:
    gc = gspread.service_account(filename=credential)
    sh = gc.open(symbol_name)
    worksheet = sh.get_worksheet(0)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    last_rows = df.tail(count)
    new_data = [{'symbol': symbol_name, 'data': date, 'hour': hour, 'NAV price': last_rows['NAV price'].mean(),
                 'last trade price': last_rows['last trade price'].mean(),
                 'deals count': last_rows['deals count'].mean(),
                 'deals volume': last_rows['deals volume'].mean(), 'final price': last_rows['final price'].mean(),
                 'total buyers count': last_rows['total buyers count'].mean(),
                 'total buyers volume': last_rows['total buyers volume'].mean(),
                 'total sellers count': last_rows['total sellers count'].mean(),
                 'total sellers volume': last_rows['total sellers volume'].mean(),
                 'individual buy volume': last_rows['individual buy volume'].mean(),
                 'individual buy count': last_rows['individual buy count'].mean(),
                 'individual sell volume': last_rows['individual sell volume'].mean(),
                 'individual sell count': last_rows['individual sell count'].mean(),
                 'corporate buy volume': last_rows['corporate buy volume'].mean(),
                 'corporate buy count': last_rows['corporate buy count'].mean(),
                 'corporate sell volume': last_rows['corporate sell volume'].mean(),
                 'corporate sell count': last_rows['corporate sell count'].mean(), }]
    df = pd.DataFrame(new_data)
    sheet_name = f'{symbol_name}_{count}'
    sh1 = gc.open(sheet_name)
    worksheet1 = sh1.get_worksheet(0)
    worksheet1.append_rows(df.values.tolist())
except EOFError as e:
    print(e)
