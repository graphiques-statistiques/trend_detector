from finance.YahooFinance import YahooFinance
from finance.TrendHistory import TrendHistory
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np


def get_tenth(lst, n):
    """
    Returns the nth tenth of a list (1-based index).
    
    Parameters:
    - lst: the list
    - n: which tenth to return (1 to 10)
    
    Returns:
    - a sublist corresponding to the nth tenth
    """
    if not 1 <= n <= 3:
        raise ValueError("n must be between 1 and 10")
    
    length = len(lst)
    start = (n - 1) * length // 3
    end = n * length // 3
    return lst[start:end]


period1 = 1726696800-10*31708800
period2 = 1770222690

# Paris
# SGO.PA, RI.PA, AI.PA, AC.PA, TTE.PA, LR.PA, BN.PA, ML.PA, AIR.PA, MT.AS, CS.PA, BNP.PA, EN.PA, BVI.PA, SU.PA,
# CAP.PA, CA.PA, ACA.PA, DSY.PA, FGR.PA, ENGI.PA, EL.PA, ERF.PA, ENX.PA, RMS.PA, KER.PA, MC.PA, ORA.PA, PUB.PA, RNO.PA, SAF.PA, SAN.PA, GLE.PA, STLA, STM, HO.PA, URW.PA, VIE.PA, DG.PA, EDEN.PA

companies = ["SGO.PA", "RI.PA", "AI.PA", "AC.PA", "TTE.PA", "LR.PA", "BN.PA", "ML.PA", "AIR.PA", "MT.AS", "CS.PA", "BNP.PA", "EN.PA", "BVI.PA", "SU.PA",
"CAP.PA", "CA.PA", "ACA.PA", "DSY.PA", "FGR.PA", "ENGI.PA", "EL.PA", "ERF.PA", "ENX.PA", "RMS.PA", "KER.PA", "MC.PA", "ORA.PA", "PUB.PA", "RNO.PA", "SAF.PA", "SAN.PA", "GLE.PA", "STLA", "STM", "HO.PA", "URW.PA", "VIE.PA", "DG.PA", "EDEN.PA"]

#for company in companies:

results = []

for company in companies:
    asset = YahooFinance(company)
    asset.get_histories(period1, period2, interval="1d")

    trend = TrendHistory(asset)
    isTrends = trend.check_trends()

    isTrends = isTrends[-30:]
    mean = np.mean(isTrends)

    if mean > 1:
        results.append(
            str(int(100 * mean / 2)) + " % " +
            asset.info["shortName"] + " | " +
            asset.info["symbol"]
        )

# Print after the loop
for result in results:
    print(result)
