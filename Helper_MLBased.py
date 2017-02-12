from marketsim import compute_portvals
from indicators import getData
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

portvolio = compute_portvals(orders_file = "./orders_ML.csv", start_val = 100000)
portvolio = portvolio/portvolio.ix[0,0]
orders=pd.read_csv("./orders_ML.csv", index_col="Date")
benchmark=getData(sd = dt.datetime(2006,1,1), ed = dt.datetime(2009,12,31), syms = ['IBM'])
benchmark=benchmark.ix[0:len(portvolio),0]
benchmark=benchmark/benchmark.ix[0,0]


long_entery=orders.ix[orders.ix[:,1]=='SELL',:]
long_entery=long_entery.ix[long_entery.ix[:,3]=='Enter', :]
long_dates=long_entery.index.tolist()

short_entery=orders.ix[orders.ix[:,1]=='BUY',:]
short_entery=short_entery.ix[short_entery.ix[:,3]=='Enter', :]
short_dates=short_entery.index.tolist()

exit_data=orders.ix[orders.ix[:,3]=='Exit',:]
exit_dates=exit_data.index.tolist()

plt.clf()
plt.plot(portvolio, c='b')
plt.plot(benchmark, c='k')
plt.legend(['port', 'bench'], loc='upper left')

for LD in long_dates:
    plt.axvline(x=LD, c='g')


for SD in short_dates:
    plt.axvline(x=SD, c='r')

for ED in exit_dates:
    plt.axvline(x=ED, c='k', linestyle='--')    
    
plt.savefig('ML_Based')

print portvolio




