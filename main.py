from scheduler import run_continuous_lazy, run_lazy
from dotenv import load_dotenv
import os
from datetime import datetime
import gspread

load_dotenv()
sheet_name = os.environ.get('SHEET_NAME', default='temp')
credential = 'credentials.json'
gc = gspread.service_account(filename=credential)
sh = gc.open(sheet_name)

sheet_names = sh.worksheets()

symbols = list(set([sheet.title[:-2].replace(' ', '_') for sheet in sheet_names]))
print(f'activating  for  symbols: {symbols}')

start_hour = int(os.environ.get('START_HOUR', default=9))
end_hour = int(os.environ.get('END_HOUR', default=15))
now = datetime.now()
end_time = now.replace(hour=end_hour - 1, minute=59, second=1)
start_time = now.replace(hour=start_hour, minute=1, second=0)
try:
    for symbol in symbols:
        run_lazy(f'./fetch_data.py {symbol}', 0, start_hour, 0, 30)
        run_continuous_lazy(f'./fetch_data.py {symbol}', 'h', 60, end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                            start_time.strftime('%Y-%m-%dT%H:%M:%S'))
        run_lazy(f'./fetch_data.py {symbol}', 0, end_hour - 1, 59, 30)
        run_continuous_lazy(f'./calc_average.py 3 ' + symbol, 'h', 180,
                            now.replace(hour=end_hour, minute=0, second=1).strftime('%Y-%m-%dT%H:%M:%S'),
                            now.replace(hour=start_hour, minute=3, second=1).strftime('%Y-%m-%dT%H:%M:%S'))
        run_continuous_lazy(f'./calc_average.py 5 {symbol}', 'h', 300,
                            now.replace(hour=end_hour, minute=0, second=1).strftime('%Y-%m-%dT%H:%M:%S'),
                            now.replace(hour=start_hour, minute=5, second=1).strftime('%Y-%m-%dT%H:%M:%S'))

except Exception as e:
    print(e)
