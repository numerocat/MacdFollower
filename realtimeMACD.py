from yahoo_fin import stock_info as si
import time
import csv
from datetime import datetime, timedelta,date
import pandas
import matplotlib.pyplot as plt
import testing
import MACD

def checkbuy(companies):

    return 0
def checksell(companies):

    return 0
def checkstaggeredsells(companies):

    return 0

def check(company,buy=True,sell=True,staggeredbuy=True):
    macd,signal,closingprices=MACD.getMACDandSignal(company)
    hist=macd-signal
    last=hist['close'].iloc[-1]
    beforelast=hist['close'].iloc[-2]
    beforebeforelast=hist['close'].iloc[-3]

    lastchange=last-beforelast # if positive, we got an increment
    changeintwodays=last-beforebeforelast

    histogramtobuy=MACD.calculateHistogramBuyValue(hist,closingprices)

    if buy==True:
        if last<histogramtobuy and lastchange>0:
            print("you should buy {} ".format(company))
    if sell==True:
        if last>0 and lastchange<0:
            print("you should sell {} ".format(company))
    if staggeredbuy==True:
        if last<histogramtobuy*0.8 and lastchange<0 and changeintwodays>0:
            print("you should do a staggered buy on {} ".format(company))
    return 0


boughlist=["apps","nflx","grwg","pfgc","pags","lrcx","kmx","acn"]
stocklist=["msft","amzn","goog","spy","fb","baba","v","jpm","arkg","voo","abt","acn","sq","czr","mtch","pags","kmx","lrcx","grwg","vale","sid","ccep","xpo","kkr","alv","halo","cx","ibp","wms","door","trox","sono","fcx","de","cnhi","auy","acgl","gshd","fdx","brp","mrvl","mu","apps","ay","nvda"]
for company in stocklist:
    #print("checking {} ".format(company))
    check(company)
 


