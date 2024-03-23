import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import random

readCache = False
showChart = False


# Input parameters

def saveTradeSimulation(sortino, type, profitFactor, symbol, tp, sl, ep, trades):
    # get dataframe from csv, if doesn't exist, create empty dataframe with columns symbol, type, profitFactor, sortino
    # add row to dataframe from the given function parameters
    # save the csv
    csv_file_path = './datadump/savedSetups.csv'

    # Check if the CSV file exists
    if os.path.exists(csv_file_path):
        # Load the existing DataFrame from CSV
        setupsDf = pd.read_csv(csv_file_path)
    else:
        # Create an empty DataFrame with the specified columns
        setupsDf = pd.DataFrame(columns=['symbol', 'type', 'profitFactor', 'sortino', 'tp', 'sl', 'ep', 'trades'])

    # Create a new row with the given parameters
    new_row = {'symbol': symbol, 'type': type, 'profitFactor': profitFactor, 'sortino': sortino, 'tp': tp, 'sl': sl,
               'ep': ep, 'trades': trades}

    # Append the new row to the DataFrame
    setupsDf = setupsDf.append(new_row, ignore_index=True)

    setupsDf = setupsDf.sort_values(by='sortino', ascending=False)

    # Save the updated DataFrame back to the CSV file
    setupsDf.to_csv(csv_file_path, index=False)


# datafile= "../../HistoricalData/Binance/BTC-01-05-2019-to-02-01-2024.csv"
# datafile = "../../HistoricalData/Binance/ETH-01-05-2019-to-02-01-2024.csv"
# datafile1m = "../../HistoricalData/Binance1m/ETH-01-05-2018-to-02-01-2024tf1m.csv"
# datafile = "../../HistoricalData/Binance/BNB-11-05-2017-to-02-01-2024.csv"
# datafile = "../../HistoricalData/Binance/BNB-01-05-2018-to-02-01-2024.csv"
# datafile1m = "../../HistoricalData/Binance1m/BNB-01-05-2018-to-02-01-2024tf1m.csv"
# datafile= "../../HistoricalData/Binance/SOL-08-05-2020-to-02-01-2024.csv"
datafile= "../../HistoricalData/Binance/XRP-01-05-2019-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/ADA-11-05-2018-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/DOGE-11-05-2019-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/AVAX-01-05-2022-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/SHIB-01-05-2022-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/TRX-01-05-2020-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/LINK-01-05-2019-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/DOT-01-05-2021-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/MATIC-01-05-2020-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/BCH-01-05-2020-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/UNI-01-05-2021-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/LTC-01-05-2018-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/ICP-01-05-2022-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/ETC-01-05-2019-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/ATOM-01-05-2020-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/FIL-01-05-2021-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/APT-01-05-2023-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/IMX-01-05-2022-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/NEAR-01-05-2021-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/STX-01-05-2021-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/INJ-01-05-2021-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/HBAR-01-05-2020-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/OP-01-05-2023-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/XLM-01-05-2021-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/VET-01-05-2019-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/GRT-01-05-2022-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/ATOM"
# datafile= "../../HistoricalData/Binance/ATOM"
# datafile= "../../HistoricalData/Binance/ATOM"

symbol = datafile[29:32]

df = pd.read_csv(datafile)
# df1m = pd.read_csv(datafile1m)

CUColor = 'green'
CDColor = 'red'

AUColor = 'blue'
ADColor = 'pink'

NUColor = 'lightGray'
NDColor = 'darkGray'

df['averageVolume'] = df['volume'].rolling(window=10).mean()
df['weirdVolume'] = df['volume'] * (df['high'] - df['low'])
df['highestWeirdVolume'] = df['weirdVolume'].rolling(window=10).max()
df['preVa'] = (df['volume'] >= df['averageVolume'] * 1.5) * 2
df['preReq'] = (df['volume'] >= df['averageVolume'] * 2) | (df['weirdVolume'] >= df['highestWeirdVolume'])
df['va'] = np.where(df['preReq'], 1, df['preVa'])

df['iff_5'] = np.where(df['va'] == 2, AUColor, NUColor)
df['iff_6'] = np.where(df['va'] == 1, CUColor, df['iff_5'])
df['iff_7'] = np.where(df['va'] == 2, ADColor, NDColor)
df['iff_8'] = np.where(df['va'] == 1, CDColor, df['iff_7'])

# df['isBull'] = df['close'] > df['open']

df['candleColor'] = np.where(df['close'] > df['open'], df['iff_6'], df['iff_8'])

df['isGreen'] = df['candleColor'] == 'green'
df['isBlue'] = df['candleColor'] == 'blue'
df['isRed'] = df['candleColor'] == 'red'
df['isPink'] = df['candleColor'] == 'pink'

# df['isColored'] = df['isGreen'] | df['isBlue'] | df['isRed'] | df['isPink']

df['redGreen'] = df['isRed'].shift() & df['isGreen']
df['redBlue'] = df['isRed'].shift() & df['isBlue']
df['pinkGreen'] = df['isPink'].shift() & df['isGreen']
df['pinkBlue'] = df['isPink'].shift() & df['isBlue']

df['buySignal'] = df['redGreen'] | df['redBlue'] | df['pinkGreen'] | df['pinkBlue']

df['greenRed'] = df['isGreen'].shift(1) & df['isRed']
df['greenPink'] = df['isGreen'].shift(1) & df['isPink']
df['blueRed'] = df['isBlue'].shift(1) & df['isRed']
df['bluePink'] = df['isBlue'].shift(1) & df['isPink']
df['sellSignal'] = df['greenRed'] | df['greenPink'] | df['blueRed'] | df['bluePink']


# df['isColoredBullish'] = df['isBlue'] | df['isGreen']
# df['isColoredBearish'] = df['isPink'] | df['isRed']

# df['topWickPercent'] = np.where(df['isBull'], (df['high'] / df['close'] - 1) * 100, (df['high'] / df['open'] - 1) * 100)
# df['bottomWickPercent'] = np.where(df['isBull'], (df['open'] / df['low'] - 1) * 100,
#                                    (df['close'] / df['low'] - 1) * 100)
# df['volumeDollars'] = df['volume'] * df['close']
#
# df['trueRange'] = abs(df['close'] - df['open'])
# df['trueRangePercent'] = abs(1 - df['close'] / df['open']) * 100
# df['averageTrueRange'] = df['trueRange'].rolling(10).sum() / 10
# df['last5Lowest'] = df['low'].rolling(5).min()
# df['last5Highest'] = df['high'].rolling(5).max()
#
# df['sma12'] = df['close'].rolling(window=20, min_periods=1).mean()
# df['diff'] = (df['sma12'] - df['close']) / df['close'] * 100
#
# df['eatsPreviousCandle'] = (df['high'] > df['high'].shift(1)) & (df['low'] < df['low'].shift(1))

def generateCacheNamePath():
    global datafile
    cacheFilename = datafile.split('/')[4].replace(".csv", "") + "-trades.csv"
    return "./datadump/caches/" + cacheFilename


def cacheTrades(trades):
    cachePath = generateCacheNamePath()
    tradesDf = pd.DataFrame(trades)
    tradesDf.to_csv(cachePath, index=False)


def simulateTrades(tpFactor, slFactor, epFactor):
    cacheNamePath = generateCacheNamePath()
    if os.path.exists(cacheNamePath) and readCache:
        return pd.read_csv(cacheNamePath).to_dict('records'), True

    currTrades = []
    trades_results = []
    lastIndex = 0

    for index, row in df.iterrows():

        lastRow = df.iloc[lastIndex]

        currTradesToRemove = []
        for trade in currTrades:

            if not trade['opened']:
                if trade['side'] == 'long':

                    if row['high'] >= trade['limit'] and row['low'] <= trade['entryLimit']:
                        trade['WL'] = 'UO'
                        trade['closeTime'] = row['close_datetime']

                        trades_results.append(trade)
                        currTradesToRemove.append(trade)

                    elif row['high'] >= trade['limit']:
                        trade['WL'] = 'MO'
                        trade['closeTime'] = row['close_datetime']

                        trades_results.append(trade)
                        currTradesToRemove.append(trade)

                    elif row['low'] <= trade['entryLimit']:
                        trade['opened'] = True

                elif trade['side'] == 'short':

                    if row['low'] <= trade['limit'] and row['high'] >= trade['entryLimit']:
                        trade['WL'] = 'UO'
                        trade['closeTime'] = row['close_datetime']

                        trades_results.append(trade)
                        currTradesToRemove.append(trade)

                    elif row['low'] <= trade['limit']:
                        trade['WL'] = 'MO'
                        trade['closeTime'] = row['close_datetime']

                        trades_results.append(trade)
                        currTradesToRemove.append(trade)

                    elif row['high'] >= trade['entryLimit']:
                        trade['opened'] = True

            if trade['opened']:

                if trade['side'] == 'long':

                    if row['high'] >= trade['limit'] and row['low'] <= trade['stop']:
                        trade['WL'] = 'NO'
                        trade['closeTime'] = row['close_datetime']

                        trades_results.append(trade)
                        currTradesToRemove.append(trade)

                    elif row['high'] >= trade['limit']:
                        trade['WL'] = 'W'
                        trade['closeTime'] = row['close_datetime']

                        trades_results.append(trade)
                        currTradesToRemove.append(trade)


                    elif row['low'] <= trade['stop']:
                        trade['WL'] = 'L'
                        trade['closeTime'] = row['close_datetime']

                        trades_results.append(trade)
                        currTradesToRemove.append(trade)

                if trade['side'] == 'short':

                    if row['low'] <= trade['limit'] and row['high'] >= trade['stop']:
                        trade['WL'] = 'NO'
                        trade['closeTime'] = row['close_datetime']

                        trades_results.append(trade)
                        currTradesToRemove.append(trade)

                    elif row['low'] <= trade['limit']:
                        trade['WL'] = 'W'
                        trade['closeTime'] = row['close_datetime']

                        trades_results.append(trade)
                        currTradesToRemove.append(trade)

                    elif row['high'] >= trade['stop']:
                        trade['WL'] = 'L'
                        trade['closeTime'] = row['close_datetime']

                        trades_results.append(trade)
                        currTradesToRemove.append(trade)

        for trade in currTradesToRemove:
            if trade in currTrades:
                currTrades.remove(trade)

        if row['buySignal']:
            entry = 'long'
            longStop = row['close'] - (row['close'] - row['low']) * slFactor
            longLimit = row['close'] + (row['close'] - row['low']) * tpFactor
            buyEntryLimit = row['close'] - (row['close'] - row['low']) * epFactor

            if buyEntryLimit != longStop:
                rr = (longLimit - buyEntryLimit) / (buyEntryLimit - longStop)

                currTrades.append({'openTime': row['close_datetime'], 'side': entry,
                                   'type': lastRow['candleColor'] + row['candleColor'], 'limit': longLimit,
                                   'stop': longStop,
                                   'entryLimit': buyEntryLimit,
                                   'opened': False,
                                   'WL': "",
                                   'closeTime': '',
                                   'rr': rr
                                   })

        elif row['sellSignal']:
            entry = 'short'
            shortStop = row['close'] + (row['high'] - row['close']) * slFactor
            shortLimit = row['close'] - (row['high'] - row['close']) * tpFactor
            sellEntryLimit = row['close'] + (row['high'] - row['close']) * epFactor

            if shortStop != sellEntryLimit:
                rr = (sellEntryLimit - shortLimit) / (shortStop - sellEntryLimit)

                currTrades.append({'openTime': row['close_datetime'], 'side': entry,
                                   'type': lastRow['candleColor'] + row['candleColor'],
                                   'limit': shortLimit,
                                   'stop': shortStop,
                                   'entryLimit': sellEntryLimit,
                                   'opened': False,
                                   'WL': "",
                                   'closeTime': '',
                                   'rr': rr})

        lastIndex = index

    print("Finished trade simulation..")

    tradesWithEssentialFilters = []
    for trade in trades_results:
        if (abs(1 - trade['limit'] / trade['stop']) / 2) * 100 < 0.20:
            tradesWithEssentialFilters.append(trade)
    for trade in tradesWithEssentialFilters:
        trades_results.remove(trade)

    return trades_results, False


def testSetup(tp, sl, ep):
    tradesResults, areResultsCached = simulateTrades(ep, sl, ep)

    if not areResultsCached:
        cacheTrades(tradesResults)

    combinations = ['redblue', 'redgreen', 'pinkblue', 'pinkgreen', 'greenred', 'greenpink', 'bluered', 'bluepink']

    for type in combinations:

        if len(tradesResults) == 0:
            continue

        currPnl = 0
        pnlChart = []
        dateChart = []

        winCount = 0
        loseCount = 0
        totalCount = 0
        notFinishedCount = 0
        uncertainOutcome = 0
        missedOpportunity = 0
        uncertainOpen = 0

        maxPnl = 0
        maxDrawdown = 0

        for trade in tradesResults:

            if trade['type'] != type:
                continue

            if trade['WL'] == "":
                notFinishedCount += 1
            if trade['WL'] == "NO":
                uncertainOutcome += 1
            if trade['WL'] == 'MO':
                missedOpportunity += 1
            if trade['WL'] == 'UO':
                uncertainOpen += 1
            if trade['WL'] == "L":
                loseCount += 1
                currPnl -= 1
            if trade['WL'] == "W":
                winCount += 1
                currPnl += round(trade['rr'], 2)

            maxPnl = max(maxPnl, currPnl)
            maxDrawdown = max(maxDrawdown, maxPnl - currPnl)

            pnlChart.append(currPnl)
            dateChart.append(str(trade['openTime']).split(" ")[0])

        if winCount == 0 or loseCount == 0:
            continue

        totalCount = winCount + loseCount + notFinishedCount + uncertainOutcome + missedOpportunity + uncertainOpen
        winRatePercent = (winCount / (winCount + loseCount)) * 100
        print(
            f'{type} win rate: {winRatePercent}%, pnl: {currPnl}, winCount: {winCount}, loseCount: {loseCount}, uncertainOutcome: {uncertainOutcome}, uncertainOpen: {uncertainOpen}, notFinishedCount: {notFinishedCount}, missedOpportunity: {missedOpportunity}, totalCount: {totalCount}')

        sortino = round(maxPnl / maxDrawdown, 2)
        profitFactor = round(winCount * tradesResults[0]['rr'] / loseCount, 2)

        saveTradeSimulation(sortino, type, profitFactor, symbol, tp, sl, ep, winCount + loseCount)

        if showChart:
            plt.figure(figsize=(16, 9))
            plt.plot(dateChart, pnlChart)
            plt.xlabel('Date')
            plt.ylabel('PnL')
            plt.title(f'{symbol} {type} PnL Over Time, win rate {winRatePercent}%')
            plt.xticks(rotation=45)
            plt.xticks(dateChart[::(len(dateChart) // min(winCount + loseCount, 40))])
            plt.grid(True, linestyle='--', color='gray', alpha=0.5)
            plt.show()

for _ in range(1000):
    tp = random.uniform(0.3, 5)
    sl = random.uniform(0.3, 2)
    ep = random.uniform(0, sl-0.1)
    testSetup(round(tp, 4), round(sl, 4), round(ep, 4))

#
# sides = ['long', 'short']
#
# for side in sides:
#     currPnl = 0
#     pnlChart = []
#     dateChart = []
#
#     winCount = 0
#     loseCount = 0
#     totalCount = 0
#     notFinishedCount = 0
#     uncertainOutcome = 0
#     missedOpportunity = 0
#     uncertainOpen = 0
#
#     for trade in tradesResults:
#
#         if trade['side'] != side:
#             continue
#
#         if trade['WL'] == "":
#             notFinishedCount += 1
#         if trade['WL'] == "NO":
#             uncertainOutcome += 1
#         if trade['WL'] == 'MO':
#             missedOpportunity += 1
#         if trade['WL'] == 'UO':
#             uncertainOpen += 1
#         if trade['WL'] == "L":
#             loseCount += 1
#             currPnl -= 1
#         if trade['WL'] == "W":
#             winCount += 1
#             currPnl += 3
#
#         pnlChart.append(currPnl)
#         dateChart.append(str(trade['openTime']).split(" ")[0])
#         totalCount = winCount + loseCount + notFinishedCount + uncertainOutcome + missedOpportunity + uncertainOpen
#         # print(trade)
#     winRatePercent = (winCount / (winCount + loseCount)) * 100
#     print(
#         f'{side} win rate: {winRatePercent}%, winCount: {winCount}, loseCount: {loseCount}, uncertainOutcome: {uncertainOutcome}, uncertainOpen: {uncertainOpen}, notFinishedCount: {notFinishedCount}, missedOpportunity: {missedOpportunity}, totalCount: {totalCount}')
#     adjustedWinCount = winCount + 2 / 3 * uncertainOpen
#     adjustedLoseCount = loseCount + 1 / 3 * uncertainOpen
#     adjustedWinRatePercent = (adjustedWinCount / (adjustedWinCount + adjustedLoseCount)) * 100
#     print(
#         f'{side} win rate: {adjustedWinRatePercent}%, winCount: {adjustedWinCount}, loseCount: {adjustedLoseCount}, uncertainOutcome: {uncertainOutcome}, uncertainOpen: {0}, notFinishedCount: {notFinishedCount}, missedOpportunity: {missedOpportunity}, totalCount: {totalCount}')
#
#     plt.plot(dateChart, pnlChart)
#
#     # Add labels and title
#     plt.xlabel('Date')
#     plt.ylabel('PnL')
#     plt.title(f'{symbol} {side} PnL Over Time, win rate {winRatePercent}%')
#
#     # Rotate x-axis labels for better readability
#     # Rotate x-axis labels for better readability
#     plt.xticks(rotation=45)
#     plt.xticks(dateChart[::(len(dateChart) // min(winCount + loseCount, 40))])
#
#     plt.grid(True, linestyle='--', color='gray', alpha=0.5)
#
#     # Show plot
#     plt.show()
#
# currPnl = 0
# pnlChart = []
# dateChart = []
#
# winCount = 0
# loseCount = 0
# totalCount = 0
# notFinishedCount = 0
# uncertainOutcome = 0
# missedOpportunity = 0
# uncertainOpen = 0
#
# for trade in tradesResults:
#
#     if trade['WL'] == "":
#         notFinishedCount += 1
#     if trade['WL'] == "NO":
#         uncertainOutcome += 1
#     if trade['WL'] == 'MO':
#         missedOpportunity += 1
#     if trade['WL'] == 'UO':
#         uncertainOpen += 1
#     if trade['WL'] == "L":
#         loseCount += 1
#         currPnl -= 1
#     if trade['WL'] == "W":
#         winCount += 1
#         currPnl += 3
#
#     pnlChart.append(currPnl)
#     dateChart.append(str(trade['openTime']).split(" ")[0])
#     totalCount = winCount + loseCount + notFinishedCount + uncertainOutcome + missedOpportunity + uncertainOpen
#     # print(trade)
# winRatePercent = (winCount / (winCount + loseCount)) * 100
# print(
#     f'All win rate: {winRatePercent}%, winCount: {winCount}, loseCount: {loseCount}, uncertainOutcome: {uncertainOutcome}, uncertainOpen: {uncertainOpen}, notFinishedCount: {notFinishedCount}, missedOpportunity: {missedOpportunity}, totalCount: {totalCount}')
# adjustedWinCount = winCount + 2 / 3 * uncertainOpen
# adjustedLoseCount = loseCount + 1 / 3 * uncertainOpen
# adjustedWinRatePercent = (adjustedWinCount / (adjustedWinCount + adjustedLoseCount)) * 100
# print(
#     f'All win rate: {adjustedWinRatePercent}%, winCount: {adjustedWinCount}, loseCount: {adjustedLoseCount}, uncertainOutcome: {uncertainOutcome}, uncertainOpen: {0}, notFinishedCount: {notFinishedCount}, missedOpportunity: {missedOpportunity}, totalCount: {totalCount}')
#
# plt.plot(dateChart, pnlChart)
#
# # Add labels and title
# plt.xlabel('Date')
# plt.ylabel('PnL')
# plt.title(f'{symbol} all trades PnL Over Time, win rate {winRatePercent}%')
#
# # Rotate x-axis labels for better readability
# plt.xticks(rotation=45)
# plt.xticks(dateChart[::min(winCount + loseCount, 40)])
#
# plt.grid(True, linestyle='--', color='gray', alpha=0.5)
#
# # Show plot
# plt.show()
