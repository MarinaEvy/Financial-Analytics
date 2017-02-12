import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from util import get_data
import warnings

warnings.simplefilter(action = "ignore", category = FutureWarning)

def getData(sd = dt.datetime(2006,1,1), ed = dt.datetime(2009,12,31), syms = ['IBM']):
    dates = pd.date_range(sd, ed)
    data= get_data(syms, dates, addSPY=False, colname = 'Adj Close')
    data=data.dropna()
    return data
    

def compute_BB(data, window=20):
    moving_average=pd.rolling_mean(data, window)
    moving_average=moving_average.dropna()
    std_MA=pd.rolling_std(data, window)
    std_MA=std_MA.dropna()
    BB_lower=moving_average-2*std_MA
    BB_upper=moving_average+2*std_MA
    BB=(data[window-1:]-moving_average)/(2*std_MA)
    plt.subplot(2, 1, 1)
    plt.plot(BB_upper)
    plt.plot(data[window:])
    plt.plot(BB_lower)
    plt.legend(['U','P', 'L'], loc='upper left')
    plt.subplot(2, 1, 2)
    plt.plot(BB)
    plt.plot()
    plt.axhline(y=1, color='r')
    plt.axhline(y=-1, color='r')
    plt.legend(['BB', 'SS', 'BS'], loc='upper left')
    plt.savefig('Bollinger_Bands')
    BB=pd.DataFrame(BB)
    BB.columns=['BB']
    return BB
    
def compute_Momentum(data, window=10):
    data_today=data[window-1:].values
    data_before=data[:-(window-1)].values
    moment=(data_today/data_before)-1
    moment=pd.DataFrame(moment)
    moment=moment.set_index(data.index.values[window-1:])
    moment.columns=['momentum']
    plt.subplot(2, 1, 1)
    plt.plot(data[window-1:])
    plt.legend(['Price'], loc='upper left')
    plt.subplot(2, 1, 2)
    plt.plot(moment)
    plt.legend(['Momentum'], loc='upper left')
    plt.savefig('momentum')
    return moment
    

def compute_SMA(data, window=20):
    SMA=pd.rolling_mean(data, window)
    SMA=SMA.dropna()
    data_t=data[window-1:]
    price_SMA=(data_t/SMA)-1
    plt.subplot(2, 1, 1)
    plt.plot(SMA)
    plt.plot(data[window-1:])
    plt.legend(['SMA','Price'], loc='upper left')
    plt.subplot(2, 1, 2)
    plt.plot(price_SMA)
    plt.legend(['(Price/SMA)-1'], loc='upper left')
    plt.savefig('SMA')
    SMA=pd.DataFrame(SMA)
    SMA.columns=['SMA']
    price_SMA = pd.DataFrame(price_SMA)
    price_SMA.columns = ['price_SMA'] 
    return SMA, price_SMA
    
    
def compute_MACD(data, low_window, high_window):
    ewma_20=pd.ewma(data, span=low_window)
    ewma_120=pd.ewma(data, span=high_window)
    macd=ewma_120-ewma_20
    signal=pd.ewma(macd, span=10)
    plt.clf()
    plt.subplot(2, 1, 1)
    plt.plot(data, c='g')
    plt.legend(['Price'], loc='upper left')
    plt.subplot(2, 1, 2)
    plt.plot(macd, c='b')
    plt.legend(['macd'], loc='upper left')
    plt.savefig('macd')
    macd=pd.DataFrame(macd)
    macd.columns = ['macd']
    signal=pd.DataFrame(signal)
    signal.columns = ['signal']
    return macd, signal

    
def compute_RSI(data,n):
    delta=data.diff()
    dUp, dDown = delta.copy(), delta.copy()
    dUp[dUp < 0] = 0
    dDown[dDown > 0] = 0
    RolUp = pd.rolling_mean(dUp, n)
    RolDown = pd.rolling_mean(dDown, n).abs()
    RS = RolUp / RolDown
    RSI= 100-100/(1+RS)   
    RSI=RSI.dropna()
    plt.subplot(2, 1, 1)
    plt.plot(data)
    plt.legend(['Price'], loc='upper left')
    plt.subplot(2, 1, 2)
    plt.plot(RSI, c='g')
    plt.legend(['RSI'], loc='upper left')
    plt.savefig('RSI')
    RSI=pd.DataFrame(RSI)
    RSI.columns = ['RSI']
    return RSI
    
        
if __name__=="__main__":
    data=getData(sd = dt.datetime(2006,1,1), ed = dt.datetime(2009,12,31), syms = ['IBM'])
    BB=compute_BB(data, 20)
    plt.clf()
    RSI=compute_RSI(data,10)
    plt.clf()
    macd, signal = compute_MACD(data, 20, 120)
    plt.clf()
    SMA, price_SMA = compute_SMA(data)
    plt.clf()
    momentum = compute_Momentum(data, 10)
    print BB
    print RSI
    print macd
    print SMA
    print price_SMA
    print momentum
    





