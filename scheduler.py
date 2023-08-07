import os
from datetime import datetime, timedelta
from threading import Timer


def run_lazy(file, day_offset=0, hour=0, minute=0, second=0, repeat=True):
    """
    Schedules a file execution

    :param file: path of file containing code to execute (relative or absolute)
    :param day_offset: day offset to repeat task, default is 1 (daily)
    :param hour: hour at which task should start
    :param minute: minute at which task should start
    :param second: second at which task should start
    :param timezone: defines timezone
    :param repeat: indicates the task should repeat continuously
    :return: nothing
    """

    def run(_day_offset, _hour, _minute, _second, _repeat):

        print('Task "%s" started at %s' % (
            file, datetime.now().strftime('%m/%d/%Y, %H:%M:%S')))
        os.system('python %s' % file)
        print('Task "%s" finished at %s' % (
            file, datetime.now().strftime('%m/%d/%Y, %H:%M:%S'),))
        if _repeat:
            exec('from scheduler import run_lazy')
            exec(
                'run_lazy("%s", %s, %s, %s, %s, %s)' % (
                    file, _day_offset, _hour, _minute, _second, _repeat))

    x = datetime.now()
    y = x.replace(day=x.day, hour=hour, minute=minute, second=second) + timedelta(days=day_offset)
    if y < x:
        y += timedelta(days=1)
    delta_t = y - x
    secs = delta_t.total_seconds()
    if secs < 0:
        print('Start time %s is passed.' % y.strftime('%m/%d/%Y, %H:%M:%S'))
    t = Timer(secs, run, kwargs={
        '_day_offset': day_offset,
        '_hour': hour,
        '_minute': minute,
        '_second': second,
        '_repeat': repeat,
    })
    t.start()
    print('"%s" is scheduled to run at %s' % (file, y.strftime('%m/%d/%Y, %H:%M:%S')))


def run_continuous_lazy(file, interval=30, end_time=None, start_time=None):
    """
    Schedules a file execution

    :param file: path of file containing code to execute (relative or absolute)
    :param interval: interval between task running in seconds, default is 30 seconds
    :param end_time: end of repeat
    :param start_time: start to repeat
    :return: nothing
    """

    def run():
        schedule()
        print('Task "%s" started at %s' % (file, datetime.now().strftime('%m/%d/%Y, %H:%M:%S')))
        os.system('python %s' % file)
        print('Task "%s" finished at %s' % (file, datetime.now().strftime('%m/%d/%Y, %H:%M:%S')))

    def schedule():
        x = datetime.now() + timedelta(seconds=interval)
        if x > end_time:
            _end_time = end_time + timedelta(days=1)
            _start_time = start_time + timedelta(days=1)
            print(_start_time.strftime("%Y-%m-%dT%H:%M:%S"))
            run_lazy(
                f'./run_continues.py {file} {interval} {_end_time.strftime("%Y-%m-%dT%H:%M:%S")} {_start_time.strftime("%Y-%m-%dT%H:%M:%S")}',
                hour=_start_time.hour, minute=_start_time.minute, second=_start_time.second, repeat=False)
            return
        t = Timer(interval, run)
        t.start()
        print('"%s" is scheduled to run at %s' % (file, x.strftime('%m/%d/%Y, %H:%M:%S')))

    start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
    end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S')

    if end_time > datetime.now() >= start_time:
        run()
    if datetime.now() > end_time:
        new_end_time = end_time + timedelta(days=1)
        new_start_time = start_time + timedelta(days=1)
        run_lazy(
            f'./run_continues.py {file} {interval} {new_end_time.strftime("%Y-%m-%dT%H:%M:%S")} {new_start_time.strftime("%Y-%m-%dT%H:%M:%S")}',
            hour=new_start_time.hour, minute=new_start_time.minute, second=new_start_time.second, repeat=False)
    elif datetime.now() < start_time:
        run_lazy(
            f'./run_continues.py {file} {interval} {end_time.strftime("%Y-%m-%dT%H:%M:%S")} {start_time.strftime("%Y-%m-%dT%H:%M:%S")}',
            hour=start_time.hour, minute=start_time.minute, second=start_time.second, repeat=False)
