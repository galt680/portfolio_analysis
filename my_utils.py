import re
import time
import holidays
import datetime

today = datetime.date.today()

def flatten(container):
    '''flatten nested containers by iterating and recursing on the conatiner'''
    flattened_list = []
    for thing in container:
        if isinstance(thing, (list, tuple)):
            for subthing in flatten(thing):
                flattened_list.append(subthing)
        else:
            flattened_list.append(thing)
    return flattened_list


def split_symbols(block_of_text):
    for sublist in range(len(block_of_text)):
        for block in block_of_text[sublist][0].splitlines():
            for individual_symbol in re.split(r''',|''', block):
                for syms in individual_symbol.split():
                    yield syms


def time_dec(func):
    def timed(*args, **kwargs):
        ts = time.time()
        result = func(*args, **kwargs)
        te = time.time()
        print(round((te - ts) / 60, 2), ' minutes')
        return result

    return timed

def is_market_day(today):
    not_holiday = today not in holidays.UnitedStates()
    isntweekend = today.weekday()
    if not_holiday and (isntweekend != 6) and (isntweekend != 5):
        return True
    else:
        return False
