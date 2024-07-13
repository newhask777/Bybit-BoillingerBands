import time
from time import sleep
import numpy as np
import talib
import matplotlib.pyplot as plt
import pandas as pd

from bybit import Bybit_api
from config import bybit_api_key, bybit_secret_key

def sleep_to_next_min():
    time_to_sleep = 60 - time.time() % 60 + 2
    print('sleep', time_to_sleep)
    time.sleep(time_to_sleep)


if __name__ == '__main__':
    client = Bybit_api(api_key=bybit_api_key, secret_key=bybit_secret_key, futures=True)

    while True:
        sleep_to_next_min()
        klines = client.get_klines(symbol="ATOMUSDT", interval="5", limit=100)
        klines = klines['result']['list']
        close_prices = [float(i[4] for i in klines)]
        close_prices_np = np.array(close_prices)
        close_prices_np = close_prices_np[::-1]
        print(close_prices_np)


        upper_band, middle_band, lower_band = talib.BBANDS(close_prices_np, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

        bollinger_df = pd.DataFrame({
            'Close': close_prices_np,
            'Upper Band': upper_band,
            'Middle Band': middle_band,
            'Lower Band': lower_band
        })

        # print(bollinger_df.tail())

        # plt.figure(figsize=(12, 6))
        # plt.plot(close_prices_np, label='Close_Price')
        # plt.plot(upper_band, label='Upper Band', linestyle='--')
        # plt.plot(middle_band, label='Middle Band', linestyle='--')
        # plt.plot(lower_band, label='Lower Band', linestyle='--')
        # plt.title('Bollinger Bands for ATOMUSDT')
        # plt.legend()
        # plt.show()


        price = bollinger_df.iloc[-1]['Close']
        ub = bollinger_df.iloc[-1]['Upper Band']
        lb = bollinger_df.iloc[-1]['Lower Band']
        print('Price', price)
        print('Upper Band:', ub)
        print('Lower Band:', lb)

        if price <lb:
            print('Long!')
            client.post_market_order(symbol='ATOMUSDT', side='buy', qnt='1')
        if price > ub:
            print('Short!')
            client.post_market_order(symbol='ATOMUSDT', side='sell', qnt=1)
        else:
            print('No signal')
