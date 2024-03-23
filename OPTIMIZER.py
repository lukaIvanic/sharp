import os
from itertools import product, combinations, chain

import pandas as pd
from CriteriaTypes import TakeProfitAnchor, StopLossAnchor, EntryCriteria
from PSVRA import getStrategyResults
import random

"""
Optimization of entry, exit
@entry -> Can always be present, can anchor off stop loss
@takeProfit -> Factor optimization doesn't have to be present, but can have different anchors like 1:1RR, previous candle open, etc.
@stopLoss -> Factor optimization doesn't have to be present, but can anchor off candle bodies, wicks, average true range, fixed value

Entry criteria
Besides the candle pattern, entry critera can be created which will filter trades taken
Multiple criterias can active at once, and a criteria can have a range of settings values

First step
Ignoring entry and exit factor optimizations, keeping only anchor choices, hard defined entry critera(s) without factor optimization.
Criteria only optimization has a finite search spectrum of under a thousand combinations, which can be solved by grid search.

Defining strategy success can be difficult, and should be thought of before running the simulations.
Ranking the strategies based on success metrics can be done after the simulations.

Metrics for strategy success should include the profit factor and maxPnl to maxDrawdown ratio for now
For every success metric there should also be an inverse, in case the strategy performs consistently to the downside.
For profit factor thats 1/profitFactor, for maxPnl to maxDrawdown ratio, it should be minPnl to maxRecovery

"""

take_profit_factors = list(TakeProfitAnchor)
stop_loss_factors = list(StopLossAnchor)
entry_parameters = list(EntryCriteria)

folderPath = "../../HistoricalData/HistoryMiddleOf2022"
csv_file_path = "./datadump/setups/optimizationSetups.csv"

allFilenamesToData = [f for f in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, f))]

entry_param_combinations = list(chain.from_iterable(combinations(entry_parameters, r) for r in range(len(entry_parameters) + 1)))

base_combinations = list(product(allFilenamesToData, take_profit_factors, stop_loss_factors))

combinations = [(datafileName, tp_factor, sl_factor, *entry_param) for (datafileName, tp_factor, sl_factor), entry_param in product(base_combinations, entry_param_combinations)]


# criteriaCombinations = list(product(allFilenamesToData, take_profit_factors, stop_loss_factors, entry_parameters))
print(f"Length of instruments: {len(allFilenamesToData)}")
print(f"Total number of iterations: {len(combinations)}")
random.shuffle(combinations)

i = 0

for combination in combinations:

    datafileName, tp_factor, sl_factor, *entry_param = combination

    results = getStrategyResults(datafileName, tp_factor, sl_factor, *entry_param)

    # print(f'Results for {tp_factor.value}-{sl_factor.value}-{entry_param.value} finished')
    if i%20 == 0:
        print(f"{round(i/len(combinations) * 100, 2)}% done..")
    i += 1


    for result in results:
        entry_param_str = '-'.join(str(param.value) for param in entry_param)
        result.insert(len(result)-1, f'{tp_factor.value}-{sl_factor.value}-{entry_param_str}')

    new_df = pd.DataFrame(results, columns=['SymbolShort', 'Type', 'ProfitFactor', 'PnLDrawdownRatio', 'ReverseProfitFactor',
                                            'ReversePnLDrawdownRatio', 'Criteria', 'OutputString'])

    if os.path.exists(csv_file_path):
        existing_df = pd.read_csv(csv_file_path)
        combined_df = pd.concat([existing_df, new_df])
    else:
        combined_df = new_df

    sorted_df = combined_df.sort_values(by='ProfitFactor', ascending=False)

    sorted_df.to_csv(csv_file_path, index=False)


