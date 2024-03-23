from itertools import product, combinations, chain
from CriteriaTypes import TakeProfitAnchor, StopLossAnchor, EntryCriteria
import os
# Assuming the Enums and lists are defined as in your setup
take_profit_factors = list(TakeProfitAnchor)
stop_loss_factors = list(StopLossAnchor)
entry_parameters = list(EntryCriteria)

folderPath = "../../HistoricalData/HistoryMiddleOf2022"
allFilenamesToData = [f for f in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, f))]

entry_param_combinations = list(chain.from_iterable(combinations(entry_parameters, r) for r in range(len(entry_parameters) + 1)))

base_combinations = list(product(allFilenamesToData, take_profit_factors, stop_loss_factors))

final_combinations = [(datafileName, tp_factor, sl_factor, *entry_param) for (datafileName, tp_factor, sl_factor), entry_param in product(base_combinations, entry_param_combinations)]

print(len(final_combinations))