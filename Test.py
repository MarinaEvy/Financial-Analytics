import pandas as pd
import datetime as dt
from indicators import getData, compute_Momentum, compute_MACD, compute_RSI
import numpy as np
import RTLearner as rt
from marketsim import compute_portvals
import matplotlib.pyplot as plt

data=getData(sd = dt.datetime(2006,1,1), ed = dt.datetime(2009,12,31), syms = ['IBM'])
data.columns=['Adj. Closed']
price=data.ix[19:len(data),:] 
price=price.as_matrix()

# compute indicators - simulate using different time windows
macd, signal = compute_MACD(data, 20, 120)
RSI = compute_RSI(data,8)
momentum = compute_Momentum(data, window=5)
X=RSI.join([momentum, macd]) 
X=X.ix[11:len(X),:]
dates=X.index.tolist()
X=X.as_matrix()

Y=np.zeros(X.shape[0])

YBUY=0.03
YSELL=-0.03
t=0 
        
Y[t]=1           
while t<(price.shape[0]-10):
    ret=(price[t+10]/price[t]) - 1.0
    if ret>YBUY:
        Y[t]=1
    elif ret < YSELL:
        Y[t] = -1 # SELL
    else:
        Y[t] = 0 # do nothing
    t=t+1

print X.shape
print Y.shape

RT=rt.RTLearner(leaf_size=5)
RT.addEvidence(X,Y)


##_________________##

#read data
data=getData(sd = dt.datetime(2010,1,1), ed = dt.datetime(2010,12,31), syms = ['IBM'])
data.columns=['Adj. Closed']
price=data.ix[19:len(data),:] 
price=price.as_matrix()

# compute indicators - simulate using different time windows
macd, signal = compute_MACD(data, 20, 120)
RSI = compute_RSI(data,8)
momentum = compute_Momentum(data, window=5)
Z=RSI.join([momentum, macd]) 
Z=Z.ix[11:len(Z),:]
dates=Z.index.tolist()
Z=Z.as_matrix()
Y_pred=RT.query(Z)
Y_pred[np.where(Y_pred<0)]=-1
Y_pred[np.where(Y_pred>0)]=1 

orders_ML=[]    
i=0
while i<(Y_pred.shape[0]):
    if Y_pred[i]==1:
        date=dates[i]
        orders_ML.append([date,'IBM' ,'BUY', 500, 'Enter'])
        if (i+10<=Y_pred.shape[0]-1): #code for exiting
            date2=dates[i+10]
            orders_ML.append([date2,'IBM', 'SELL', 500, 'Exit'])
            i=i+10
        else:
            date2=dates[Y_pred.shape[0]-1]
            orders_ML.append([date2,'IBM', 'SELL', 500, 'Exit'])
            i=i+10
    elif Y_pred[i]==-1:
        date=dates[i]
        orders_ML.append([date,'IBM' ,'SELL', 500, 'Enter'])
        if (i+10<=Y_pred.shape[0]-1): #code for exiting
            date2=dates[i+10]
            orders_ML.append([date2,'IBM', 'BUY', 500, 'Exit'])
            i=i+10
        else:
            date2=dates[Y_pred.shape[0]-1]
            orders_ML.append([date2,'IBM', 'BUY', 500, 'Exit'])
            i=i+10   
    else:
        i=i+1
        
orders_ML_Test=pd.DataFrame(orders_ML)
orders_ML_Test=orders_ML_Test.set_index(orders_ML_Test.ix[:,0])
orders_ML_Test=orders_ML_Test.ix[:,1:4]
orders_ML_Test.index.name='Date'
orders_ML_Test.columns=['Symbol',	'Order',	'Shares', 'Enter or Exit']
orders_ML_Test.to_csv('orders_ML_Test.csv', sep=',')


portvolio_ML = compute_portvals(orders_file = "./orders_ML_Test.csv", start_val = 100000)
portvolio_ML=portvolio_ML.ix[2:len(portvolio_ML),0]
portvolio_ML = portvolio_ML/portvolio_ML.ix[0,0]
benchmark=getData(sd = dt.datetime(2010,1,1), ed = dt.datetime(2010,12,31), syms = ['IBM'])
benchmark=benchmark.ix[21:len(portvolio_ML),0]
benchmark=benchmark/benchmark.ix[0,0]

#----------------------------------------------------


data=getData(sd = dt.datetime(2010,1,1), ed = dt.datetime(2010,12,31), syms = ['IBM'])
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
orders_RB_Test=pd.DataFrame(orders_RB)
orders_RB_Test=orders_RB_Test.set_index(orders_RB_Test.ix[:,0])
orders_RB_Test=orders_RB_Test.ix[:,1:4]
orders_RB_Test.index.name='Date'
orders_RB_Test.columns=['Symbol','Order','Shares','Enter or Exit']
orders_RB_Test.to_csv('orders_RB_Test.csv', sep=',')

portvolio_RB = compute_portvals(orders_file = "./orders_RB_Test.csv", start_val = 100000)
portvolio_RB = portvolio_RB/portvolio_RB.ix[0,0]


plt.clf()
plt.axis([dt.datetime(2010,2,03), dt.datetime(2010,12,01), 0.9, 1.28])
plt.plot(portvolio_RB, c='b')
plt.plot(benchmark, c='k')
plt.plot(portvolio_ML, c='g')
plt.legend(['port_RB', 'bench', 'port_ML'], loc='upper left')
plt.savefig('Test')


def assessPort(prices):
    prices=pd.DataFrame(prices)
    cr=(prices.ix[len(prices)-1]/prices.ix[0])-1
    dr=prices.copy()
    dr[1:]=(prices.ix[1:]/prices.ix[:-1].values)-1
    dr.ix[0]=0
    adr=dr[1:].sum()/(len(dr)-1)
    sddr=dr[1:].std()
    sr=((adr-0)/sddr)*252**0.5
    return cr, adr, sddr, sr

cr_ML, adr_ML, sddr_ML, sr_ML = assessPort(portvolio_ML)
cr_RB, adr_RB, sddr_RB, sr_RB = assessPort(portvolio_RB)
cr_B, adr_B, sddr_B, sr_B = assessPort(benchmark)

print portvolio_RB
print portvolio_ML
print benchmark

print "Sharpe Ratio_ML:", sr_ML
print "Volatility (stdev of daily returns)_ML:", sddr_ML
print "Average Daily Return_ML:", adr_ML
print "Cumulative Return_ML:", cr_ML

print "Sharpe Ratio_RB:", sr_RB
print "Volatility (stdev of daily returns)_RB:", sddr_RB
print "Average Daily Return_RB:", adr_RB
print "Cumulative Return_RB:", cr_RB


print "Sharpe Ratio_B:", sr_B
print "Volatility (stdev of daily returns)_B:", sddr_B
print "Average Daily Return_B:", adr_B
print "Cumulative Return_B:", cr_B
