import pandas as pd
import datetime as dt
from indicators import getData, compute_Momentum, compute_MACD, compute_RSI
import numpy as np
import RTLearner as rt


#read data
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

RT=rt.RTLearner(leaf_size=4)
RT.addEvidence(X,Y)
Y_pred=RT.query(X)
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
        
orders_ML=pd.DataFrame(orders_ML)
orders_ML=orders_ML.set_index(orders_ML.ix[:,0])
orders_ML=orders_ML.ix[:,1:4]
orders_ML.index.name='Date'
orders_ML.columns=['Symbol',	'Order',	'Shares', 'Enter or Exit']
orders_ML.to_csv('orders_ML.csv', sep=',')


