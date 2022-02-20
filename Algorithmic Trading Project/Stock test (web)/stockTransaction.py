# 1. Scraping  Teams
import requests
from bs4 import BeautifulSoup

# 2. Accessing Stock data
from datetime import datetime, timedelta
import pandas_datareader.data as web


# 3. Forming DataFrame
import pandas as pd


import codeChecker

def stockDataGetter(codes, startDate, endDate):
    codeStatus = {                                     # Open, close, and volume
    "code": [],
    "date": [],
    "codeOpen ($)": [],
    "codeClose ($)": [],
    "codeVolume": []
    }
    
    errorCode = []    

    for code in codes:
        try:
            data = web.DataReader(code, "yahoo", startDate, endDate)               # Stock_code, search_engine, start_date, end_date
            # 要最新果日 (SCRARPE TIME: 香港時間 2022/01/29 01:20 AM, 但用"2022-01-28", "2022-01-29" 會顯示出27, 28 日的價(可能是時差問題))
            
            # Attracting the number of rows from the dataset
            for i in range(data.shape[0]):                         # according to its number of row
                stockDate = data["Date"][i]                        # newly added, maybe wrong
                stockOpen = data["Open"][i]
                stockClose = data["Close"][i]
                stockVolume = data["Volume"][i]
                        
                codeStatus["code"].append(code)
                codeStatus["date"].append(stockDate)
                codeStatus["codeOpen ($)"].append(stockOpen)
                codeStatus["codeClose ($)"].append(stockClose)
                codeStatus["codeVolume"].append(stockVolume)
        
        except:
            errorCode.append(code)
                        
    return pd.DataFrame(codeStatus)
