from yahoo_fin import stock_info as si
import time
import csv
from datetime import datetime, time
import pandas
import matplotlib.pyplot as plt
import testing
import MACD
import mock

buyprice=4

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def ismultiplied(company,buyprice,multiplier=2):
    price=si.get_live_price(company)

    if price>buyprice*multiplier:
        return True
    else:
        return False
def round_decimal(number, decimal_places=2):
    decimal_value = Decimal(number)
    return decimal_value.quantize(Decimal(10) ** -decimal_places)

def getincrease(company,buyprice):
    price=si.get_live_price(company)
    return round_decimal(price/buyprice)


companylist=[]

company1 = {"ticker": "amc","price": 4}
company2 = {"ticker": "gme","price": 6}
companylist.append(company1)
companylist.append(company2)

while True:

    if not is_time_between(time(11,40), time(16,30)):
        print("NOT IN TIME RANGE, FINISHING THE PROCESS")
        break

    for company in companylist:
        increase=getincrease(company["ticker"],company["buyprice"])
        if increase>2.5:
            print("company {} increased {} !!!".format(company["ticker"],increase))
            
    time.sleep(60*10)



    
    

        




    
    
    
    




    
    
