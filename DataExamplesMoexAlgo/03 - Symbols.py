import datetime as dt
import backtrader as bt
from backtrader_moexalgo.moexalgo_store import MoexAlgoStore  # Storage AlgoPack
from Strategy import StrategyJustPrintsOHLCVAndSuperCandles  # Trading System

# Multiple tickers for multiple trading systems on the same time interval history + live
if __name__ == '__main__':  # Entry point when running this script
    
    symbols = ('SBER', 'AFLT')  # tickers for which we will receive data

    store = MoexAlgoStore()  # Storage AlgoPack
    cerebro = bt.Cerebro(quicknotify=True)  # Initiating the "engine" BackTrader

    for _symbol in symbols:  # Running through all the tickers

        # 1. Historical 5-minute bars for the last 100 hours + Chart because offline/ M5 timeframe
        fromdate = dt.datetime.utcnow() - dt.timedelta(minutes=100*60)  # we take data for the last 100 hours
        data = store.getdata(timeframe=bt.TimeFrame.Minutes, compression=5, dataname=_symbol, fromdate=fromdate, live_bars=False)

        # 2. Historical 1-minute bars for the last hour + new live bars / M1 timeframe
        # fromdate = dt.datetime.utcnow() - dt.timedelta(minutes=60)  # we take the data for the last 1 hour
        # data = store.getdata(timeframe=bt.TimeFrame.Minutes, compression=1, dataname=_symbol, fromdate=fromdate, live_bars=True)

        # 3. Historical 1-hour bars for the week + Chart because offline/ timeframe H1
        # fromdate = dt.datetime.utcnow() - dt.timedelta(hours=24*7)  # we take the data for the last week from the current time
        # data = store.getdata(timeframe=bt.TimeFrame.Minutes, compression=60, dataname=_symbol, fromdate=fromdate, live_bars=False)

        cerebro.adddata(data)  # Adding data

    cerebro.addstrategy(StrategyJustPrintsOHLCVAndSuperCandles)  # Adding a trading system

    cerebro.run()  # Launching a trading system
    cerebro.plot()  # Draw a chart !!! IF we have not received any data from the market, then here it will be AttributeError: 'Plot_OldSync' object has no attribute 'mpyplot'
