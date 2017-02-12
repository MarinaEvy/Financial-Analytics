
import pandas as pd
import datetime as dt
from indicators import getData, compute_Momentum, compute_MACD, compute_RSI


#read data
data=getData(sd = dt.datetime(2006,1,1), ed = dt.datetime(2009,12,31), syms = ['IBM'])
data.columns=['Adj. Closed']


# compute indicators - simulate using different time windows
momentum = compute_Momentum(data, window=5)
macd, signal = compute_MACD(data, 20, 120)
RSI = compute_RSI(data,8)

ind=RSI.join([momentum, macd, data])  #dataframe containing all the indicators and adjusted closed prices

orders_RB=[] # orders list - dates symbol order shares (shares=500)
dates=ind.index.tolist() # list that contains the trading dates


i=0
while i<len(ind):
    if (ind.ix[i,2]<0 and ind.ix[i,0]<=40 and ind.ix[i, 1]<0):
        date=dates[i]
        orders_RB.append([date,'IBM' ,'BUY', 500, 'Enter'])
        if (i+10<=len(ind)-1): #code for exiting
            date2=dates[i+10]
            orders_RB.append([date2,'IBM', 'SELL', 500, 'Exit'])
            i=i+10
        else:
            date2=dates[(len(ind)-1)]
            orders_RB.append([date2,'IBM', 'SELL', 500, 'Exit'])
            i=i+10
    elif (ind.ix[i,2]>0 and ind.ix[i,0]>=50 and ind.ix[i,1]>0):
        date=dates[i]
        orders_RB.append([date,'IBM' ,'SELL', 500, 'Enter'])
        if (i+10<=len(ind)-1): # code for exiting
            date2=dates[i+10]
            orders_RB.append([date2,'IBM', 'BUY', 500, 'Exit'])
            i=i+10
        else:
            date2=dates[(len(ind)-1)]
            orders_RB.append([date2,'IBM', 'BUY', 500, 'Exit'])
            i=i+10
    else:
        i=i+1
    
        
# convert orders list to dataframe and prepare orders.csv file for marketsim
orders_RB=pd.DataFrame(orders_RB)
orders_RB=orders_RB.set_index(orders_RB.ix[:,0])
orders_RB=orders_RB.ix[:,1:4]
orders_RB.index.name='Date'
orders_RB.columns=['Symbol','Order','Shares','Enter or Exit']
orders_RB.to_csv('orders_RB.csv', sep=',')



print ind