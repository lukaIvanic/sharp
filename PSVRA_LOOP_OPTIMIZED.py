import pandas as pd
import numpy as np
from CriteriaTypes import TakeProfitAnchor, StopLossAnchor, EntryCriteria
import time

symbolShort = ""
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


def precalculateTpSl(df, tpCriteria, slCriteria):
    if slCriteria is StopLossAnchor.CURR_CANDLE_WICK:
        df['stop'] = np.where(df['isBull'], df['low'], df['high'])
    elif slCriteria is StopLossAnchor.PREV_CANDLE_WICK:
        df['stop'] = np.where(df['isBull'], df['low'].shift(1), df['high'].shift(1))
    elif slCriteria is StopLossAnchor.CURR_CANDLE_BODY:
        df['stop'] = df['open']

    if tpCriteria is TakeProfitAnchor.PREV_CANDLE_OPEN:
        df['limit'] = df['open'].shift(1)
    elif tpCriteria is TakeProfitAnchor.PREV_CANDLE_WICK:
        df['limit'] = np.where(df['isBull'], df['high'].shift(1), df['low'].shift(1))
    elif tpCriteria is TakeProfitAnchor.ONE_TO_ONE_RR:
        df['limit'] = np.where(df['isBull'], df['close'] + (df['close'] - df['stop']),
                               df['close'] - (df['stop'] - df['close']))


def precalculateTooSmallTrade(df):
    df['buySignal'] = np.where(df['buySignal'], ~(((df['limit'] - df['close']) / df['close'] * 100 < 0.2) | (
            (df['close'] - df['stop']) / df['close'] * 100 < 0.2)), df['buySignal'])

    df['sellSignal'] = np.where(df['sellSignal'], ~(((df['stop'] - df['close']) / df['close'] * 100 < 0.2) | (
            (df['close'] - df['limit']) / df['close'] * 100 < 0.2)), df['sellSignal'])


def precalculateRR(df):
    """
       rr = (longLimit - row['close']) / (row['close'] - longStop)


            rr = (row['close'] - shortLimit) / (shortStop - row['close'])
    """

    df['rr'] = np.where(df['buySignal'], (df['limit'] - df['close']) / (df['close'] - df['stop']), np.nan)
    df['rr'] = np.where(df['sellSignal'], (df['close'] - df['limit']) / (df['stop'] - df['close']), df['rr'])


def runTradeStrategy(datafileName,
                     takeProfitAnchor: TakeProfitAnchor,
                     stopLossAnchor: StopLossAnchor,
                     *entryCriteria: EntryCriteria):
    railwayCheck = EntryCriteria.RAILWAY_CHECK in entryCriteria
    outOfChannelCheck = EntryCriteria.OUT_OF_CHANNEL_CHECK in entryCriteria

    startTime = time.time()

    df = getDf(datafileName)

    precalculateTpSl(df, takeProfitAnchor, stopLossAnchor)
    precalculateTooSmallTrade(df)
    precalculateRR(df)

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

    trades_results = []

    buySignals = df[df['buySignal']]

    endTime = time.time()
    print(f"Vectorization execTime: {endTime - startTime} seconds")
    startTime = endTime

    for startCandleIndex, startCandle in buySignals.iterrows():

        trade = {
            'openTime': startCandle['close_datetime'],
            'side': 'long',
            'type': df.iloc[startCandleIndex - 1]['candleColor'] + startCandle['candleColor'],
            'limit': startCandle['limit'], 'stop': startCandle['stop'],
            'WL': "", 'closeTime': '', 'rr': startCandle['rr']
        }

        for i in range(startCandleIndex + 1, len(df)):
            current_row = df.iloc[i]

            # if startCandle['isBull']:
            if current_row['high'] >= trade['limit'] and current_row['low'] <= trade['stop']:
                trade['WL'] = 'NA'
                trade['closeTime'] = current_row['close_datetime']

                trades_results.append(trade)
                break

            elif current_row['high'] >= trade['limit']:
                trade['WL'] = 'W'
                trade['closeTime'] = current_row['close_datetime']

                trades_results.append(trade)
                break


            elif current_row['low'] <= trade['stop']:
                trade['WL'] = 'L'
                trade['closeTime'] = current_row['close_datetime']

                trades_results.append(trade)
                break


    sellSignals = df[df['sellSignal']]

    for startCandleIndex, startCandle in sellSignals.iterrows():

        trade = {
            'openTime': startCandle['close_datetime'],
            'side': 'short',
            'type': df.iloc[startCandleIndex - 1]['candleColor'] + startCandle['candleColor'],
            'limit': startCandle['limit'], 'stop': startCandle['stop'],
            'WL': "", 'closeTime': '', 'rr': startCandle['rr']
        }

        for i in range(startCandleIndex + 1, len(df)):
            current_row = df.iloc[i]

            if current_row['low'] <= trade['limit'] and current_row['high'] >= trade['stop']:
                trade['WL'] = 'NA'
                trade['closeTime'] = current_row['close_datetime']

                trades_results.append(trade)
                break

            elif current_row['low'] <= trade['limit']:
                trade['WL'] = 'W'
                trade['closeTime'] = current_row['close_datetime']

                trades_results.append(trade)
                break

            elif current_row['high'] >= trade['stop']:
                trade['WL'] = 'L'
                trade['closeTime'] = current_row['close_datetime']

                trades_results.append(trade)
                break


    endTime = time.time()
    print(f"For loop execution time: {endTime - startTime} seconds")

    return trades_results


def getCriteriaString(tpAnchor, slAnchor):
    return tpAnchor.value + "-" + slAnchor.value


def saveToCsv(tradesResults, datafileName, criteraShortName):
    csvName = f"./datadump/results/new/{datafileName}-{criteraShortName}.csv"

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


startTime = time.time()

getStrategyResults("ALGO-01-05-202-to-06-15-2022.csv", TakeProfitAnchor.ONE_TO_ONE_RR, StopLossAnchor.CURR_CANDLE_WICK)
getStrategyResults("ALGO-01-05-202-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_WICK,
                   StopLossAnchor.CURR_CANDLE_WICK)
getStrategyResults("ALGO-01-05-202-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_OPEN,
                   StopLossAnchor.CURR_CANDLE_WICK)
getStrategyResults("ALGO-01-05-202-to-06-15-2022.csv", TakeProfitAnchor.ONE_TO_ONE_RR, StopLossAnchor.PREV_CANDLE_WICK)
getStrategyResults("ALGO-01-05-202-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_WICK,
                   StopLossAnchor.PREV_CANDLE_WICK)
getStrategyResults("ALGO-01-05-202-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_OPEN,
                   StopLossAnchor.PREV_CANDLE_WICK)
getStrategyResults("ALGO-01-05-202-to-06-15-2022.csv", TakeProfitAnchor.ONE_TO_ONE_RR, StopLossAnchor.CURR_CANDLE_BODY)
getStrategyResults("ALGO-01-05-202-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_WICK,
                   StopLossAnchor.CURR_CANDLE_BODY)
getStrategyResults("ALGO-01-05-202-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_OPEN,
                   StopLossAnchor.CURR_CANDLE_BODY)

getStrategyResults("BNB-01-05-2018-to-06-15-2022.csv", TakeProfitAnchor.ONE_TO_ONE_RR, StopLossAnchor.CURR_CANDLE_WICK)
getStrategyResults("BNB-01-05-2018-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_WICK,
                   StopLossAnchor.CURR_CANDLE_WICK)
getStrategyResults("BNB-01-05-2018-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_OPEN,
                   StopLossAnchor.CURR_CANDLE_WICK)
getStrategyResults("BNB-01-05-2018-to-06-15-2022.csv", TakeProfitAnchor.ONE_TO_ONE_RR, StopLossAnchor.PREV_CANDLE_WICK)
getStrategyResults("BNB-01-05-2018-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_WICK,
                   StopLossAnchor.PREV_CANDLE_WICK)
getStrategyResults("BNB-01-05-2018-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_OPEN,
                   StopLossAnchor.PREV_CANDLE_WICK)
getStrategyResults("BNB-01-05-2018-to-06-15-2022.csv", TakeProfitAnchor.ONE_TO_ONE_RR, StopLossAnchor.CURR_CANDLE_BODY)
getStrategyResults("BNB-01-05-2018-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_WICK,
                   StopLossAnchor.CURR_CANDLE_BODY)
getStrategyResults("BNB-01-05-2018-to-06-15-2022.csv", TakeProfitAnchor.PREV_CANDLE_OPEN,
                   StopLossAnchor.CURR_CANDLE_BODY)

endTime = time.time()

executionTime = endTime - startTime

print(f"Execution time for new script {executionTime} seconds")
