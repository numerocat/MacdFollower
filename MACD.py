from yahoo_fin import stock_info as si
import time
import csv
from datetime import datetime, timedelta,date
import pandas
import matplotlib.pyplot as plt
import testing
import numpy as np

plt.style.use("fivethirtyeight")

def Average(lst): 
    return sum(lst) / len(lst) 

def make_plot(slope):
    x = np.arange(1,10)
    y = slope*x+3
    plt.figure()
    plt.plot(x,y)

def getMACDandSignal(company,shortspan=9,longspan=26):
    closingprices=si.get_data(company)["close"][-800:].to_frame()
    shortema=closingprices.ewm(span=shortspan,adjust=False).mean()
    longema=closingprices.ewm(span=longspan,adjust=False).mean()
    MACD=shortema-longema
    signal=MACD.ewm(span=9,adjust=False).mean()
    return MACD,signal,closingprices

def calculateprofit(company,shortspan=9,longspan=26,showprints=False):
    MACD, signal,closingprices=getMACDandSignal(company,shortspan,longspan)
    #closingprices=si.get_data(company)["close"].to_frame()
    hist=MACD-signal
    histogram=hist.drop(hist.index[:30])    
    owned=False
    profitlist=[]
    buyprice=0
    firstbuyprice=0
    sellprice=0
    profit=0
    startingmoney=1000
    trades=0
    timemoneyisonstock=0
    money=startingmoney
    buyday=timedelta(days=1)
    firstbuyday=timedelta(days=1)
    sellday=timedelta(days=1)
    initialtime=None
    startingtocount=0
    twodaysbefore=0
    threedaysbefore=0
    buydates=[]
    selldates=[]
    buys=[]
    sells=[]
    buyhistogramvalue=-1000
    sharesowned=0
    buyshares=1
    Staggeredbuyshares=buyshares*2
    totalbuy=0
    for index,row in histogram.iterrows():

        if startingtocount==0:
            startingtocount=startingtocount+1
            twodaysbefore=row[0]

        elif startingtocount==1:
            startingtocount=startingtocount+1
            threedaysbefore=row[0]
        else:
            if initialtime is None:
                initialtime=index.to_pydatetime().date()


            changeinoneday=(row[0]-twodaysbefore)
            changethedaybefore=(twodaysbefore-threedaysbefore)
            changeintwodays=(row[0]-threedaysbefore)

            
            
                
            if owned==True:
                if row[0]>0 and changeinoneday<0: # Si tenemos un decremento, vendemos todo

                    sellday=index+timedelta(days=1)
                    sellprice=testing.getpriceinaday(closingprices,sellday)
                    if sellprice>firstbuyprice:
                        profit=(sellprice*sharesowned-totalbuy)/totalbuy
                        money=money*(1+profit)
                        owned=False
                        trades=trades+1
                        days=(sellday-firstbuyday).days
                        timemoneyisonstock=timemoneyisonstock+days
                        if showprints==True:
                            print("sold for {}  profit and for {} days".format(profit*100,days))
                        selldates.append(sellday)
                        sells.append(sellprice)
                        totalbuy=0
                        sharesowned=0
                        buyhistogramvalue=-1000


                #daytocheckhistogram = hist.index.get_loc(index)
                #histogramvalue=calculateHistogramBuyValue(hist,closingprices,daytocheckhistogram)
                #print("buyhistogramvalue: ",buyhistogramvalue)
                #print("row[0]: ",row[0])
                if row[0]<buyhistogramvalue*0.8 and changeinoneday>0: # Compra escalonada

                    buyday=index+timedelta(days=1)
                    buyprice=testing.getpriceinaday(closingprices,buyday)
                    if showprints==True:
                        print("buying AGAIN at {} in {} with a histogramvalue of {} ".format(buyprice,buyday,row[0]))
                    buydates.append(buyday)
                    buys.append(buyprice)
                    buyhistogramvalue=row[0]
                    totalbuy=Staggeredbuyshares*buyprice+totalbuy
                    sharesowned=sharesowned+Staggeredbuyshares # incrementing number of shares owned

            else:
                
                daytocheckhistogram = hist.index.get_loc(index)
                histogramvalue=calculateHistogramBuyValue(hist,closingprices,daytocheckhistogram) ## Solo se debera llamar cuando sea <0 ya que sino podriamos estar
                                                                                                  ## hallando el chiste para cuando estamos en histtograma verde y asi contar
                                                                                                  ## uno de los tramos como si ya lo hubieramos terminado 
                
                if row[0]<=histogramvalue and changeinoneday>0: # Cuando hay un aumento en el histograma, comprar
                    firstbuyday=index+timedelta(days=1)
                    firstbuyprice=testing.getpriceinaday(closingprices,firstbuyday)
                    owned=True
                    if showprints==True:
                        print("buying at {} in {} with a histogramvalue of {} ".format(firstbuyprice,firstbuyday,row[0]))
                    buydates.append(firstbuyday)
                    buys.append(firstbuyprice)
                    buyhistogramvalue=row[0]
                    totalbuy=buyshares*firstbuyprice
                    sharesowned=sharesowned+buyshares
            threedaysbefore=twodaysbefore
            twodaysbefore=row[0]

    #print("money: ", money)
    profit=100*(money-startingmoney)/startingmoney
    print("trades: {} and a total time of {} days".format(trades,timemoneyisonstock))
    print("starting date {} it means {} days ".format(initialtime,(date.today()-initialtime).days))
            
    return profit,selldates,buydates,sells,buys

def calculateHistogramBuyValue(hist,closingprices,dateposition=None):
    if dateposition is None:
        dateposition=len(hist.index)-1
    histogramtouse=hist[:dateposition+1]
    #print("closingtype: ",type(closingprices))
    #print("closingprices: ",closingprices)
    prices=closingprices[:dateposition+1]
    #print("hist: ",hist)
    #print("closingprices: ",closingprices)
    #print("############################")
    #print("histogramtouse: ",histogramtouse)
    #print("prices: ",prices)
    
    #print("dateposition: ",dateposition)
    #print("histogramtouse DESPUES: ",histogramtouse)
    #print(histogramtouse)
    # Calcula el valor por el cual deberias comprar, este sera un promedio de los puntos mas bajos en un tiempo
    # Se entrega un hist que es un pandas.core.frame.DataFrame con los valores de histograma hasta la fecha para la cual quieres hallar el valor del histograma para comprar
    # 
    Starting=True
    Calculatetime=False
    negativeslist=[]
    bestnegative=0
    finishedtrail=True
    selldate=0
    buydate=0
    buyprice=0
    sellprice=0
    maxvalue=0
    minvalue=0
    daysperpercentagelist=[]
    minlist=[]
    value=0
    

    for i in range(1,70): # Segun esto hallaremos los valores desde el ultimo hasta el primero como si fuera: [-1]
        #print("i: ",i)
        valueposition=i*-1
        #print("date: ",histogramtouse.index[-i])

        # Separar cada uno de los tramos negativos
        # Extraer el valor minimo
        # Extraer un promedio de esa lista
        try:
            histogramvalue=histogramtouse.loc[ : , 'close' ][valueposition]
            #print("histogramvalue: ",histogramvalue)
        except:
            continue

        if Starting==True: # at first lets wait till we get a positive histogram to get sell date
            if histogramvalue<0:
                continue
            if histogramvalue>0:
                Starting=False
                maxvalue=histogramvalue
                exn=histogramvalue
                selldate=histogramtouse.index[valueposition]
                sellprice=testing.getpriceinaday(prices,selldate)
                #print("starting in {} and with an histogram value of {} and price: {} ".format(histogramtouse.index[valueposition],str(histogramvalue),sellprice))

        elif Starting==False:

            if histogramvalue<0:
                if histogramvalue<minvalue: # Simulate a buy
                    buydate=histogramtouse.index[valueposition]
                    buyprice=testing.getpriceinaday(prices,buydate)
                    exn=histogramvalue
                    minvalue=histogramvalue
                    #print("simulating a buy and having a histogram of {}  in {} and price {} ".format(str(histogramvalue),buydate,buyprice))

            if histogramvalue>0 and exn<0:# finish a trail and simulate a sell because we are starting everything
                #print("sellprice: ",sellprice)
                #print("buyprice: ",buyprice)
                gain=100*(sellprice-buyprice)/buyprice
                days=(selldate-buydate).days
                daysperpercentage=days/gain
                

                if daysperpercentage<1: # If we need 3 days for 1% gain, give this minimun value
                    daysperpercentagelist.append(daysperpercentage)
                    minlist.append(minvalue)
                else:
                    daysperpercentagelist.append(daysperpercentage)
                    if minvalue*2<value: 
                        value=minvalue*2
                minvalue=0
                maxvalue=histogramvalue
                selldate=histogramtouse.index[valueposition]
                sellprice=testing.getpriceinaday(prices,selldate)
                exn=histogramvalue

            if histogramvalue>0 and exn>0:# Simulate a sell
                if histogramvalue>maxvalue:
                    selldate=histogramtouse.index[valueposition]
                    sellprice=testing.getpriceinaday(prices,selldate)
                    exn=histogramvalue
                    maxvalue=histogramvalue
                    #print("simulating a sell and having a histogram of {}  in {} and price {} ".format(str(histogramvalue),selldate,sellprice))
    
    if len(minlist)>0:
        value=max(minlist)

    return value




"""
# Take a list with the companies we are about to check
companies=[]
df=pandas.read_csv("companylist.csv")
print("companies: ",companies)
# Main algorithm
for company in companies:
    difference=MACD(company)-signal(company)
    if difference>0:
        print("buy ", company)
    if difference<0:
        print("sell ", company)
"""
def showMACDSignalComparisson(company,selldates=None,buydates=None,sells=None,buys=None):
    # Use for only one company, it will give you a plot of the comparisson
    # Example: showMACDSignalComparisson("dht")
    MACD, signal,prices=getMACDandSignal(company)
    histogramplot=plt.figure(num=1)
    pricessize=len(prices.index)

    plt.plot(prices.index,MACD,label="{} macd".format(company),color="red")
    plt.plot(prices.index,signal,label="{} signal".format(company),color="blue")
    plt.plot(prices.index,MACD-signal,label="{} histogram".format(company),color="green")
    yclist=[0]*pricessize #horizontal line
    plt.plot(prices.index,yclist,label="histogram=0".format(company),color="brown")
    plt.xticks(rotation=10)
    plt.legend(loc="upper left")

    stockpriceplot=plt.figure(num=2)
    plt.plot(prices.index,prices["close"],label="{} stock price".format(company),alpha=0.5)
    if selldates is not None:
        plt.scatter(buydates,buys,color="green",label="buy",marker="^",alpha=1)
        plt.scatter(selldates,sells,color="red",label="sell",marker="x",alpha=1)
    plt.xticks(rotation=10)

    plt.show()
    
    





i=0
if i==1:
    #stocklist=[company]
    stocklist=["msft","amzn","goog","spy","jnj","fb","baba","v","jpm"]
    wins=0
    for stock in stocklist:
        numberofcompanies=len(stocklist)
        #print(" {}  has an MACD profit of: {} ".format(stock,calculateprofit(stock)))
        closingprices=si.get_data(stock)["close"].to_frame()
        pricebefore=testing.getpriceinaday(closingprices,"2017-03-23 00:00:00")
        pricenow=si.get_live_price(stock)
        profit=(pricenow-pricebefore)*100/pricebefore
        macdprofit,selldates,buydates,sells,buys=calculateprofit(stock,showprints=False)
        print(" {} had a MACD profit of: {}%%  and normal profit of {}% ".format(stock,macdprofit,profit))
        print("###################################################")
        if macdprofit>profit:
            wins=wins+1
    print("wins: ", wins,"/",numberofcompanies)

#showMACDSignalComparisson(company,selldates,buydates,sells,buys)
