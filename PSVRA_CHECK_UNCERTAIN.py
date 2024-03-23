import pandas as pd
import os

oneMinuteFilePath = "../../HistoricalData/Binance1m/ETH-01-05-2018-to-02-01-2024tf1m"
oneMinuteFilePathCsv = oneMinuteFilePath + ".csv"
oneMinuteFilePathParquet = oneMinuteFilePath + ".parquet"


def get1mDataframe():
    if os.path.exists(oneMinuteFilePathParquet):
        print("Reading parquet file.")
        return pd.read_parquet(oneMinuteFilePathParquet)
    else:
        print("Converting CSV to Parquet.")
        dfCsv = pd.read_csv(oneMinuteFilePathCsv, parse_dates=['close_datetime'], index_col='close_datetime')
        dfCsv.to_parquet(oneMinuteFilePathParquet)
        print("Finished conversion.")
        return dfCsv


df1m = get1mDataframe()

tradesDf = pd.read_csv('./datadump/caches/ETH-01-05-2019-to-02-01-2024-trades.csv')

print("Iterating through rows..")
tradesDf['closeTime'] = pd.to_datetime(tradesDf['closeTime'])
countWin = 0
countLose = 0
for index, trade in tradesDf.iterrows():
    # I have row['closeTime'] and I need to find the row with the same time df1m['closed_datetime']
    # Then, I need to take that row and the 14 candles before that from df1m
    # Then, I need to check which happened first in those 15 candles (they are already sorted with respect to time),
    # if candles['high'] > row['limit'] was first or candles['low'] < row['stop'] was first
    # This process needs to optimized as much as possible

    if trade['WL'] != 'UO' and trade['WL'] != 'NO':
        continue

    close_time = trade['closeTime']
    open_time = trade['openTime']

    if '2021-08-08 02:14:59' in str(open_time):
        print("Evo ga")

    # Find the corresponding row in df1m and 14 candles before it
    if close_time in df1m.index:
        start_time = max(df1m.index.get_loc(close_time) - 14, 0)
        relevant_candles = df1m.iloc[start_time: df1m.index.get_loc(close_time) + 1]

        if trade['side'] == 'long':
            # Check conditions
            LBChecks = relevant_candles['low'] <= trade['entryLimit']
            LSChecks = relevant_candles['high'] >= trade['limit']
            SLChecks = relevant_candles['low'] <= trade['stop']

            limitBuyCross = LBChecks.idxmax() if LBChecks.any() else None
            limitSellCross = LSChecks.idxmax() if LSChecks.any() else None
            stopSellCross = SLChecks.idxmax() if SLChecks.any() else None

            if limitBuyCross is None or limitSellCross is None:
                continue

            if stopSellCross is None and limitBuyCross < limitSellCross:
                tradesDf.at[index, 'WL'] = 'W'
            if stopSellCross is not None and limitSellCross < limitBuyCross and limitSellCross < stopSellCross:
                tradesDf.at[index, 'WL'] = 'MO'
            if stopSellCross is None and limitSellCross < limitBuyCross:
                tradesDf.at[index, 'WL'] = 'MO'
            elif stopSellCross is not None and limitBuyCross < limitSellCross < stopSellCross:
                tradesDf.at[index, 'WL'] = 'W'
            elif stopSellCross is not None and stopSellCross < limitSellCross:
                tradesDf.at[index, 'WL'] = 'L'
            elif stopSellCross is not None and limitBuyCross == limitSellCross:
                tradesDf.at[index, 'WL'] = 'NO'
            elif stopSellCross is None and limitBuyCross == limitSellCross:
                tradesDf.at[index, 'WL'] = 'UO'



        elif trade['side'] == 'short':

            LSChecks = relevant_candles['high'] >= trade['entryLimit']
            LBChecks = relevant_candles['low'] <= trade['limit']
            SBChecks = relevant_candles['high'] >= trade['stop']

            limitSellCross = LSChecks.idxmax() if LSChecks.any() else None
            limitBuyCross = LBChecks.idxmax() if LBChecks.any() else None
            stopBuyCross = SBChecks.idxmax() if SBChecks.any() else None

            if limitSellCross is None or limitBuyCross is None:
                continue

            if stopBuyCross is None and limitSellCross < limitBuyCross:
                tradesDf.at[index, 'WL'] = 'W'
            elif stopBuyCross is not None and limitSellCross < limitBuyCross < stopBuyCross:
                tradesDf.at[index, 'WL'] = 'W'
            elif stopBuyCross is not None and limitBuyCross < limitSellCross and limitBuyCross < stopBuyCross:
                tradesDf.at[index, 'WL'] = 'MO'
            elif stopBuyCross is None and limitBuyCross < limitSellCross:
                tradesDf.at[index, 'WL'] = 'MO'
            elif stopBuyCross is not None and stopBuyCross < limitBuyCross:
                tradesDf.at[index, 'WL'] = 'L'
            elif stopBuyCross is not None and limitSellCross == limitBuyCross:
                tradesDf.at[index, 'WL'] = 'NO'
            elif stopBuyCross is None and limitSellCross == limitBuyCross:
                tradesDf.at[index, 'WL'] = 'UO'

tradesDf.to_csv('./datadump/caches/ETH-01-05-2019-to-02-01-2024-tradesChecked.csv')
