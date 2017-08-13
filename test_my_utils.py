import time
from datetime import date
from my_utils import is_market_day







def test_is_market_day():
    assert is_market_day(date(2017,1,1)) == False
    assert is_market_day(date(2017,1,2)) == False
    assert is_market_day(date(2017,1,3)) == True
    assert is_market_day(date(2017,1,4)) == True
    assert is_market_day(date(2017,1,7)) == False
    assert is_market_day(date(2017,1,8)) == False
    assert is_market_day(date(2017,1,9)) == True
