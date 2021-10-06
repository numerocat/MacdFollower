from yahoo_fin import stock_info as si
import time
import csv
from datetime import datetime, timedelta,date
import pandas
""" TO DO:
    - save results in .csv file
    - create a trading script
"""
def incomegrowth(income_statement):
    # income_statement can be set like income_statement=si.get_income_statement("FB") if you are using yearly stuff, if not, specify income_statement=si.get_income_statement("FB",yearly=False)
    # Returns income growth year over year or q over q, if the yearly parameter is False it will return q over q
    # The order is going to be: (last income growth, one year before, 2 years bf.)
    incomegrowthlist=[]
    incomelist=incomeinlast4periods(income_statement)
    for i in range(len(incomelist)-1):
        incomegrowthlist.append((incomelist[i]-incomelist[i+1])*100/(incomelist[i+1]+0.0001))
    return incomegrowthlist

def incomeinlast4periods(income_statement):
    # The order is: (last year, 1 year before, 2 years before)
    incomelist=[]
    revenues=income_statement.loc[["totalRevenue"],:]
    for j in range(len(revenues.iloc[0])):
        incomelist.append(revenues.iloc[0][j]) 
    return incomelist

def getcurrentratio(ticker):
    return si.get_stats(ticker)["Value"][46]

def getpriceinaday(closingpricesdataframe,day):
    result=None
    while result is None:

        try:
            result=closingpricesdataframe.loc[[day],:].iloc[0][0]
        except:
            #print("could not find price for day: ", day)
            day=day-timedelta(days=1)
            #print("trying for day: ", day)

    return result
            
def returninanumberofdays(ticker,daysback):
    actualprice=si.get_live_price(ticker)
    closingprices=si.get_data(ticker)["close"].to_frame()
    day=date.today()-timedelta(days=daysback)
    pricetocompare=getpriceinaday(closingprices,day)
    
    return 100*(actualprice-pricetocompare)/pricetocompare

def savetotxt(file_name,listtosave):
    with open(file_name, 'w') as f:
        for item in listtosave:
            f.write("%s\n" % item)


###### Testing
#st=si.get_income_statement("ALIN-PA")
#print(st)
#st=si.get_income_statement("ALTG",yearly=False)
#print(st)

###### Main algorith
winnerslist=[]
i=0
if i==1:
    statement=0
    threshold=10 # To get percentage completed
    df=pandas.read_csv("companylist.csv")
    companieslist=df["Symbol"].tolist()
    total=len(companieslist)
    print("total companies: "+ str(total))
    i=0
    for company in companieslist:
        i=i+1

        print("checking company: ", company)

        try:
            statement=si.get_income_statement(company)
        except:
            print("Error: could not retrieve data for this company")
            pass

        if all(growth>10 for growth in incomegrowth(statement)):
            print("nice")
            winnerslist.append(str(company))

        if i*100/total>threshold:
            print("###########################################1########################################################")
            print(str(threshold)+"%")
            print("###########################################1########################################################")
            threshold=threshold+10

    savetotxt("firstwinners.txt",winnerslist)
j=0
if j==1:
    companies=[]
    f = open('winnerslist.txt','r')
    for line in f:
        companies.append(line.strip())
    print("companies: ", companies)
    winnerslist=companies

    i=0
    threshold=10
    total=len(winnerslist)
    print("total companies: "+ str(total))
    for company in winnerslist:
        i=i+1
        statement=si.get_income_statement(company,yearly=False)
        print("checking company: ", company)

        if not all(growth>10 for growth in incomegrowth(statement)):
            print("filtered by q growth")
            winnerslist.remove(company)
            continue

        if getcurrentratio(company)<2:
            winnerslist.remove(company)
            print("filtered by current ratio ")
            continue

        if returninanumberofdays(company,7)<0 or returninanumberofdays(company,30)<0:
            print("filtered by return un 7 or 30 days")
            winnerslist.remove(company)
            continue


        if i*100/total>threshold:
            print("###########################################2########################################################")
            print(str(threshold)+"%")
            print("###########################################2########################################################")
            threshold=threshold+10


            
        






