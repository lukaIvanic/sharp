import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from CriteriaTypes import TakeProfitAnchor, StopLossAnchor, EntryCriteria
import time

"""
    if not skipLargeDifferenceCheck:
        df['trueRange'] = abs(df['close'] - df['open'])

        df['firstCandleTooLarge'] = (df['trueRange'].shift(1) / df['trueRange']) > 5

        df['buySignal'] = df['buySignal'] & ~df['firstCandleTooLarge']
        df['sellSignal'] = df['sellSignal'] & ~df['firstCandleTooLarge']

    if not skipTooSmallCheck:
        df['averageTrueRange'] = df['trueRange'].rolling(window=11, min_periods=1).mean()

        df['isTooSmall'] = ((df['trueRange'] + df['trueRange'].shift(1)) / 2) < (df['averageTrueRange'] * 0.7)

        df['buySignal'] = df['buySignal'] & ~df['isTooSmall']
        df['sellSignal'] = df['sellSignal'] & ~df['isTooSmall']

    if not skipSecondCandleSmallerCheck:
        df['isNicePattern'] = df['trueRange'] < (df['trueRange'].shift(1) * 1.3)

        df['buySignal'] = df['buySignal'] & df['isNicePattern']
        df['sellSignal'] = df['sellSignal'] & df['isNicePattern']
"""

# datafile= "../../HistoricalData/Binance/BTC-01-05-2019-to-02-01-2024.csv"
datafile = "../../HistoricalData/HistoryMiddleOf2022/ETH-01-05-2019-to-06-15-2022.csv"
# datafile = "../../HistoricalData/Binance/BNB-11-05-2017-to-02-01-2024.csv"
# datafile= "../../HistoricalData/Binance/SOL-08-05-2020-to-02-01-2024.csv"
# datafile = "../../HistoricalData/Binance/XRP-01-05-2019-to-02-01-2024.csv"
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

symbolShort = ""
showCharts = False
df = None

def getDf(datafileName):
    global df, symbolShort

    df = pd.read_csv(f"../../HistoricalData/HistoryMiddleOf2022/{datafileName}")

    symbolShort = datafileName[:3]

    CUColor = 'green'
    CDColor = 'red'

    AUColor = 'blue'
    ADColor = 'pink'

    NUColor = 'lightGray'
    NDColor = 'darkGray'

    lookbackPeriod = 10

    df['averageVolume'] = df['volume'].rolling(window=lookbackPeriod).mean()
    df['weirdVolume'] = df['volume'] * (df['high'] - df['low'])
    df['highestWeirdVolume'] = df['weirdVolume'].rolling(window=lookbackPeriod).max()
    df['preVa'] = (df['volume'] >= df['averageVolume'] * 1.5) * 2
    df['preReq'] = (df['volume'] >= df['averageVolume'] * 2) | (df['weirdVolume'] >= df['highestWeirdVolume'])
    df['va'] = np.where(df['preReq'], 1, df['preVa'])

    df['iff_5'] = np.where(df['va'] == 2, AUColor, NUColor)
    df['iff_6'] = np.where(df['va'] == 1, CUColor, df['iff_5'])
    df['iff_7'] = np.where(df['va'] == 2, ADColor, NDColor)
    df['iff_8'] = np.where(df['va'] == 1, CDColor, df['iff_7'])

    df['isBull'] = df['close'] > df['open']

    df['candleColor'] = np.where(df['isBull'], df['iff_6'], df['iff_8'])

    df['isGreen'] = df['candleColor'] == 'green'
    df['isBlue'] = df['candleColor'] == 'blue'
    df['isRed'] = df['candleColor'] == 'red'
    df['isPink'] = df['candleColor'] == 'pink'

    df['isColored'] = df['isGreen'] | df['isBlue'] | df['isRed'] | df['isPink']

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

    return df


def runTradeStrategy(datafileName,
                     takeProfitAnchor: TakeProfitAnchor,
                     stopLossAnchor: StopLossAnchor,
                     *entryCriteria: EntryCriteria):
    railwayCheck = EntryCriteria.RAILWAY_CHECK in entryCriteria
    outOfChannelCheck = EntryCriteria.OUT_OF_CHANNEL_CHECK in entryCriteria

    df = getDf(datafileName)

    if railwayCheck:
        df['isColoredBullish'] = df['isBlue'] | df['isGreen']
        df['isColoredBearish'] = df['isPink'] | df['isRed']

        df['isRailway'] = (df['buySignal'] & df['isColoredBullish'].shift(2)) | (
                df['sellSignal'] & df['isColoredBearish'].shift(2))
        df['buySignal'] = df['buySignal'] & ~df['isRailway']
        df['sellSignal'] = df['sellSignal'] & ~df['isRailway']

    if outOfChannelCheck:
        df['highestLast5'] = df['high'].rolling(window=6, min_periods=1).max()
        df['lowestLast5'] = df['low'].rolling(window=6, min_periods=1).min()

        isOutOfChannel = (df['buySignal'] & (df['close'].shift(1) < df['lowestLast5'].shift(2))) | (
                df['sellSignal'] & (df['close'].shift(1) > df['highestLast5'].shift(2)))

        df['buySignal'] = df['buySignal'] & isOutOfChannel
        df['sellSignal'] = df['sellSignal'] & isOutOfChannel

    currTrades = []

    trades_results = []

    lastIndex = 0

    # print("Finished vector operations")

    for index, row in df.iterrows():

        lastRow = df.iloc[lastIndex]

        currTradesToRemove = []
        for trade in currTrades:

            if trade['side'] == 'long':

                if row['high'] >= trade['limit'] and row['low'] <= trade['stop']:
                    trade['WL'] = 'NA'
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
                    trade['WL'] = 'NA'
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

            longStop = 0

            if stopLossAnchor is StopLossAnchor.CURR_CANDLE_WICK:
                longStop = row['low']
            elif stopLossAnchor is StopLossAnchor.PREV_CANDLE_WICK:
                longStop = lastRow['low']
            elif stopLossAnchor is StopLossAnchor.CURR_CANDLE_BODY:
                longStop = row['open']

            longLimit = 0

            if takeProfitAnchor is TakeProfitAnchor.PREV_CANDLE_OPEN:
                if row['close'] > lastRow['open']:
                    lastIndex = index
                    continue
                longLimit = lastRow['open']
            elif takeProfitAnchor is TakeProfitAnchor.PREV_CANDLE_WICK:
                if row['close'] > lastRow['high']:
                    lastIndex = index
                    continue
                longLimit = lastRow['high']
            elif takeProfitAnchor is TakeProfitAnchor.ONE_TO_ONE_RR:
                longLimit = row['close'] + (row['close'] - longStop)

            if (longLimit - row['close']) / row['close'] * 100 < 0.2 or (row['close'] - longStop) / row['close'] * 100 < 0.2:
                lastIndex = index
                continue

            rr = (longLimit - row['close']) / (row['close'] - longStop)

            currTrades.append({'openTime': row['close_datetime'], 'side': entry,
                               'type': lastRow['candleColor'] + row['candleColor'],
                               'limit': longLimit, 'stop': longStop,
                               'WL': "", 'closeTime': '',
                               'rr': rr})

        elif row['sellSignal']:
            entry = 'short'

            shortStop = 0

            if stopLossAnchor is StopLossAnchor.CURR_CANDLE_WICK:
                shortStop = row['high']
            elif stopLossAnchor is StopLossAnchor.PREV_CANDLE_WICK:
                shortStop = lastRow['high']
            elif stopLossAnchor is StopLossAnchor.CURR_CANDLE_BODY:
                shortStop = row['open']

            shortLimit = 0

            if takeProfitAnchor is TakeProfitAnchor.PREV_CANDLE_OPEN:

                if row['close'] < lastRow['open']:
                    lastIndex = index
                    continue

                shortLimit = lastRow['open']

            elif takeProfitAnchor is TakeProfitAnchor.PREV_CANDLE_WICK:

                if row['close'] < lastRow['low']:
                    lastIndex = index
                    continue

                shortLimit = lastRow['low']

            elif takeProfitAnchor is TakeProfitAnchor.ONE_TO_ONE_RR:
                shortLimit = row['close'] - (shortStop - row['close'])

            if (shortStop - row['close']) / row['close'] * 100 < 0.2 or (row['close'] - shortLimit) / row['close'] * 100 < 0.2:
                lastIndex = index
                continue

            rr = (row['close'] - shortLimit) / (shortStop - row['close'])

            currTrades.append({'openTime': row['close_datetime'], 'side': entry,
                               'type': lastRow['candleColor'] + row['candleColor'],
                               'limit': shortLimit, 'stop': shortStop,
                               'WL': "", 'closeTime': '',
                               'rr': rr})
        lastIndex = index


    return trades_results

def getCriteriaString(tpAnchor, slAnchor):
    return tpAnchor.value + "-" + slAnchor.value



def saveToCsv(tradesResults, datafileName, criteraShortName):
    csvName = f"./datadump/results/old/{datafileName}-{criteraShortName}.csv"

    tradesDf = pd.DataFrame(tradesResults)

    tradesDf.to_csv(csvName)

    print(f"saved trade results to {csvName}")



def getStrategyResults(
                    datafileName,
                    takeProfitAnchor: TakeProfitAnchor,
                     stopLossAnchor: StopLossAnchor,
                     *entryCriteria: EntryCriteria):

    tradesResults = runTradeStrategy(datafileName,
                                    takeProfitAnchor,
                                     stopLossAnchor,
                                     *entryCriteria)

    saveToCsv(tradesResults, datafileName, getCriteriaString(takeProfitAnchor, stopLossAnchor))

    combinations = ['redblue', 'redgreen', 'pinkblue', 'pinkgreen', 'greenred', 'greenpink', 'bluered', 'bluepink']
    results = []

    for type in combinations:
        currPnl = 0
        pnlChart = []
        dateChart = []

        winCount = 0
        loseCount = 0
        totalCount = 0
        notFinishedCount = 0
        uncertainOutcome = 0

        grossLoss = 0
        grossWin = 0

        maxPnl = 0
        maxDrawdown = 0

        minPnl = 0
        maxRecovery = 0

        for trade in tradesResults:

            if trade['type'] != type:
                continue

            if trade['WL'] == "":
                notFinishedCount += 1
            if trade['WL'] == "NA":
                uncertainOutcome += 1
            if trade['WL'] == "L":
                loseCount += 1
                currPnl -= 1
                grossLoss += 1
            if trade['WL'] == "W":
                winCount += 1
                currPnl += trade['rr']
                grossWin += trade['rr']

            maxPnl = max(currPnl, maxPnl)
            maxDrawdown = max(maxPnl - currPnl, maxDrawdown)

            minPnl = min(currPnl, minPnl)
            maxRecovery = max(currPnl - minPnl, maxRecovery)

            pnlChart.append(currPnl)
            dateChart.append(str(trade['openTime']).split(" ")[0])
        # print(
        #     f'{type} win rate: {(winCount / (winCount + loseCount)) * 100}%, winCount: {winCount}, loseCount: {loseCount}, uncertainOutcome: {uncertainOutcome}, notFinishedCount: {notFinishedCount} totalCount: {totalCount}, endPnl: {currPnl}')

        profitFactor = grossWin / grossLoss if grossLoss != 0 else grossWin
        pnlDrawdownRatio = maxPnl / maxDrawdown if maxDrawdown != 0 else maxPnl

        reverseProfitFactor = 1 / profitFactor if profitFactor != 0 else grossLoss
        reversePnlDrawdownRatio = minPnl / maxRecovery if maxRecovery != 0 else minPnl

        totalCount = winCount + loseCount + notFinishedCount + uncertainOutcome

        if totalCount >= 100:
            results.append([symbolShort, type, round(profitFactor, 2), round(pnlDrawdownRatio, 2), round(reverseProfitFactor, 2), round(reversePnlDrawdownRatio, 2), f'{round((winCount / (winCount + loseCount)) * 100, 2) if winCount + loseCount != 0 else 0}%-uO:{uncertainOutcome}-tC:{totalCount}'])

        if showCharts:
            plt.figure(figsize=(16, 9))
            plt.plot(dateChart, pnlChart)
            plt.xlabel('Date')
            plt.ylabel('PnL')
            plt.title(f'{symbolShort} {type} PnL Over Time')
            plt.xticks(rotation=45)
            plt.xticks(dateChart[::(len(dateChart) // min(40, len(dateChart)))])
            plt.grid(True, linestyle='--', color='gray', alpha=0.5)
            plt.show()

    return results

startTime = time.time()




getStrategyResults("ALGO-01-05-202-to-06-15-2022.csv", TakeProfitAnchor.ONE_TO_ONE_RR, StopLossAnchor.CURR_CANDLE_WICK)
getStrategyResults("ALGO-01-05-202-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_WICK, StopLossAnchor.CURR_CANDLE_WICK)
getStrategyResults("ALGO-01-05-202-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_OPEN, StopLossAnchor.CURR_CANDLE_WICK)
getStrategyResults("ALGO-01-05-202-to-06-15-2022.csv", TakeProfitAnchor.ONE_TO_ONE_RR, StopLossAnchor.PREV_CANDLE_WICK)
getStrategyResults("ALGO-01-05-202-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_WICK, StopLossAnchor.PREV_CANDLE_WICK)
getStrategyResults("ALGO-01-05-202-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_OPEN, StopLossAnchor.PREV_CANDLE_WICK)
getStrategyResults("ALGO-01-05-202-to-06-15-2022.csv", TakeProfitAnchor.ONE_TO_ONE_RR, StopLossAnchor.CURR_CANDLE_BODY)
getStrategyResults("ALGO-01-05-202-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_WICK, StopLossAnchor.CURR_CANDLE_BODY)
getStrategyResults("ALGO-01-05-202-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_OPEN, StopLossAnchor.CURR_CANDLE_BODY)

getStrategyResults("BNB-01-05-2018-to-06-15-2022.csv", TakeProfitAnchor.ONE_TO_ONE_RR, StopLossAnchor.CURR_CANDLE_WICK)
getStrategyResults("BNB-01-05-2018-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_WICK, StopLossAnchor.CURR_CANDLE_WICK)
getStrategyResults("BNB-01-05-2018-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_OPEN, StopLossAnchor.CURR_CANDLE_WICK)
getStrategyResults("BNB-01-05-2018-to-06-15-2022.csv", TakeProfitAnchor.ONE_TO_ONE_RR, StopLossAnchor.PREV_CANDLE_WICK)
getStrategyResults("BNB-01-05-2018-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_WICK, StopLossAnchor.PREV_CANDLE_WICK)
getStrategyResults("BNB-01-05-2018-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_OPEN, StopLossAnchor.PREV_CANDLE_WICK)
getStrategyResults("BNB-01-05-2018-to-06-15-2022.csv", TakeProfitAnchor.ONE_TO_ONE_RR, StopLossAnchor.CURR_CANDLE_BODY)
getStrategyResults("BNB-01-05-2018-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_WICK, StopLossAnchor.CURR_CANDLE_BODY)
getStrategyResults("BNB-01-05-2018-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_OPEN, StopLossAnchor.CURR_CANDLE_BODY)


endTime = time.time()

executionTime = endTime-startTime

print(f"Execution time for old script {executionTime} seconds")











# #
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
#
#     for trade in tradesResults:
#
#         if trade['side'] != side:
#             continue
#
#         if trade['WL'] == "":
#             notFinishedCount += 1
#         if trade['WL'] == "NA":
#             uncertainOutcome += 1
#         if trade['WL'] == "L":
#             loseCount += 1
#             currPnl -= 1
#         if trade['WL'] == "W":
#             winCount += 1
#             currPnl += 1
#
#         pnlChart.append(currPnl)
#         dateChart.append(str(trade['openTime']).split(" ")[0])
#         totalCount = winCount + loseCount + notFinishedCount + uncertainOutcome
#         # print(trade)
#     print(
#         f'{side} win rate: {(winCount / (winCount + loseCount)) * 100}%, winCount: {winCount}, loseCount: {loseCount}, uncertainOutcome: {uncertainOutcome}, notFinishedCount: {notFinishedCount} totalCount: {totalCount}')
#
#     plt.plot(dateChart, pnlChart)
#
#     # Add labels and title
#     plt.xlabel('Date')
#     plt.ylabel('PnL')
#     plt.title(f'{symbol} {side} PnL Over Time')
#
#     # Rotate x-axis labels for better readability
#     plt.xticks(rotation=45)
#     plt.xticks(dateChart[::(len(dateChart) // 40)])
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
#
# for trade in tradesResults:
#
#     if trade['WL'] == "":
#         notFinishedCount += 1
#     if trade['WL'] == "NA":
#         uncertainOutcome += 1
#     if trade['WL'] == "L":
#         loseCount += 1
#         currPnl -= 1
#     if trade['WL'] == "W":
#         winCount += 1
#         currPnl += 1
#
#     pnlChart.append(currPnl)
#     dateChart.append(str(trade['openTime']).split(" ")[0])
#     totalCount = winCount + loseCount + notFinishedCount + uncertainOutcome
#     # print(trade)
# print(
#     f'All trades win rate: {(winCount / (winCount + loseCount)) * 100}%, winCount: {winCount}, loseCount: {loseCount}, uncertainOutcome: {uncertainOutcome} notFinishedCount: {notFinishedCount} totalCount: {totalCount}')
#
# plt.plot(dateChart, pnlChart)
#
# # Add labels and title
# plt.xlabel('Date')
# plt.ylabel('PnL')
# plt.title(f'{symbol} all trades PnL Over Time')
#
# # Rotate x-axis labels for better readability
# plt.xticks(rotation=45)
# plt.xticks(dateChart[::50])
#
# plt.grid(True, linestyle='--', color='gray', alpha=0.5)
#
# # Show plot
# plt.show()
