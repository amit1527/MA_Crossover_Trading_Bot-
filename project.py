from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, TakeProfitRequest, StopLossRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderClass
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
import pandas as pd
import time
from config import API_KEY, SECRET_KEY #Custom Library to Maintain Account Privacy
client = TradingClient(API_KEY, SECRET_KEY)


#Calling Main Function To Activate Bot
def main():
    while True: #Using while loop To Execute Bot repeatedly until error occur
        try:
            trading_job()
        except Exception as e:
            print("Error:", e)

        time.sleep(60)  # Run every 60 seconds



def get_data():
    data_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)#This Function Fetch Historical Data from Broker

    #Fetching Minute Data of given Ticker
    req_para = StockBarsRequest(
        symbol_or_symbols='AMZN', #Ticker or Stock symbol
        feed='iex',
        timeframe=TimeFrame.Minute , # minute data
        start=datetime(2025, 1,1), #start sate
        end=datetime.now() #current Time
    )

    bar = data_client.get_stock_bars(req_para)
    df = bar.df.reset_index()

    df = df.drop(['symbol','trade_count', 'vwap'], axis=1) #Removing Unnecessory columns from Dataframe
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')

    df['ma1'] = round(df['close'].rolling(60).mean(), 3 ) #Making 1 hour moving Avg or Rolling Window
    df['ma6'] = round(df['close'].rolling(360).mean(),3) #Making 6 hour moving Avg or Rolling Window


    df['pre_ma1']= df['ma1'].shift(1) #Shifting Previous Moving Avg upward

    df=df.dropna()

    return df

df = get_data()


def trading_signal(ma1:float, ma6 : float, pre_ma1:float): #Generating Trade Signals

    #Bullish signal --> 1
    if (ma1 >= ma6) and (pre_ma1<ma6):
        return 1

    #Bearish signal --> 0
    elif (ma1 <= ma6) and (pre_ma1 >ma6):
        return 0

    #no signal --> -1
    else:
        return -1

df['crossover'] = df.apply(
    lambda row: trading_signal(row['ma1'], row['ma6'], row['pre_ma1']),
    axis=1
) # Making A saperate Column for Signal generated from each candle



def trading_job():
    ratio = 2 #Risk n Riward Ratio

    ma1 = df.iloc[-1]['ma1'] #1hr Moving Avg Value of very latest candle
    ma6 = df.iloc[-1]['ma6'] #6hr Moving Avg Value of very latest candle
    pre_ma1 = df.iloc[-1]['pre_ma1'] #pre 1hr Moving Avg Value of very latest candle
    signal = trading_signal(ma1, ma6, pre_ma1)

    #Buy side SL and TP
    y = df[-101:-1]['low'].min()
    x = df.iloc[-1]['open']
    diff = abs(x-y)
    buy_sl = df.iloc[-1]['open'] - diff
    buy_tp = df.iloc[-1]['open'] + diff*ratio

    #Sell side SL and TP
    ys = df[-101:-1]['high'].min()
    diff_s = abs(ys-x)
    sell_sl = df.iloc[-1]['open'] + diff
    sell_tp = df.iloc[-1]['open'] - diff*ratio

    #sell
    if signal == 0:
        mo= MarketOrderRequest(
                    symbol="AMZN",
                    qty=100, #Quantity
                    side=OrderSide.SELL, #sell side order or bearish order
                    time_in_force=TimeInForce.DAY,
                    order_class=OrderClass.BRACKET,
                    take_profit=TakeProfitRequest(limit_price = sell_tp), #setting Take Profit
                    stop_loss=StopLossRequest(stop_price=sell_sl) #setting Stop Loss
                    )

        bracket_order = client.submit_order(order_data=mo) # Submitting order
        print(df.iloc[-1:,:])
        print(f"Open : {x}", " ", f"TPsell : {sell_tp}", " ", f"SLsell : {sell_sl}")

    #Buy
    elif signal == 1:
        mo= MarketOrderRequest(
                    symbol="AMZN",
                    qty=100,#Quantity
                    side=OrderSide.BUY, #buy side order or bullish order
                    time_in_force=TimeInForce.DAY,
                    order_class=OrderClass.BRACKET,
                    take_profit=TakeProfitRequest(limit_price=buy_tp), #setting Take Profit
                    stop_loss=StopLossRequest(stop_price=buy_sl) #setting Stop Loss
                    )

        bracket_order = client.submit_order(order_data=mo) # Submitting order
        print(df.iloc[-1:,:])
        print(f"Open : {x}", " ", f"TPbuy : {buy_tp}", " ", f"SLbuy: {buy_sl}")

    #NO signal
    else:
        print("OOPS, NO SIGNAL NO TRADE!!")

if __name__ == "__main__":
    main()

