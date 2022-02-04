"""

Business logic:

1. scrape code from the web by HTTP request 
2. For loop with code in pandas to get data 
3. Save it in table and send to database (Or excel) ... storing the code status: append code into code 

# for append being pass to pandas and show in tables

"""

# 1. Scraping  Teams
import requests
from bs4 import BeautifulSoup
import string
import re


# 2. Accessing Stock data
from datetime import datetime, timedelta
import pandas_datareader.data as web

# 3. Forming DataFrame
import pandas as pd

#-----------------------------------------------------------------------------------------------


# Part 1: Getting the US Stock Code 

codes = []                                  # store codes
letters = list(string.ascii_uppercase)      # Setting A-Z letter list 

print("\033[1;32;1m Executing Mission 1 ... \033[0m\n")     # Green color for signal

for letter in letters:
    url = f"https://eoddata.com/stocklist/NASDAQ/{letter}.htm"          # Capital A-Z according to web's pattern
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'lxml')                           # turn into DOM structure
    
    # filter with special pattern: stockquote/NASDAQ/...
    tags = soup.find_all("a", href=re.compile("/stockquote/NASDAQ/"))   # regular expression for specified searching 

    for t in tags: 
        if (t.string is not None):
                codes.append(t.string)
                
print("\033[1;32;1m Mission 1 Complete ! \033[0m\n") 

#-----------------------------------------------------------------------------------------------

# Part 2: Access data from pandas

count = 0                                          # successful searching
errorCount = 0                                     # fail searching

endDate = datetime.now()                           # Current time system (your computer)
startDate = endDate - timedelta(days=1)            # Two days before current (your computer)

str_endDate = endDate.strftime("%Y-%m-%d")         # date obj. to string   
str_startDate = startDate.strftime("%Y-%m-%d")     
errorCode = []                                     # append to list

codeStatus = {                                     # Open, close, and volume
    "code": [],
    "date": [],
    "codeOpen ($)": [],
    "codeClose ($)": [],
    "codeVolume": []
    }

print("\033[1;32;1m Executing Mission 2 ... \033[0m\n")

for code in codes:
    try:
        data = web.DataReader(code, "yahoo", str_startDate, str_endDate)               # Stock_code, search_engine, start_date, end_date
        # 要最新果日 (SCRARPE TIME: 香港時間 2022/01/29 01:20 AM, 但用"2022-01-28", "2022-01-29" 會顯示出27, 28 日的價(可能是時差問題))
        
        # Attracting the number of rows from the dataset
        for i in range(data.shape[0]):                         # according to its number of row
            stockDate = data.index[i].strftime("%Y-%m-%d")                           # newly added, maybe wrong
            stockOpen = data["Open"][i]
            stockClose = data["Close"][i]
            stockVolume = data["Volume"][i]
    
            codeStatus["code"].append(code)
            codeStatus["date"].append(stockDate)
            codeStatus["codeOpen ($)"].append(stockOpen)
            codeStatus["codeClose ($)"].append(stockClose)
            codeStatus["codeVolume"].append(stockVolume)
        
        print(f" Successful: {code}")
          
    except:
        print(f"\033[1;31m Has probelems on -----{code} \033[0m")          # red color for fail 
        errorCode.append(code)
        
        
print("\033[1;32;1m Mission 2 Complete ! \033[0m\n")

#----------------------------------------------------------------------------------------------

# Part 3: Convert Dict to DataFrame and export to CSV file

print("\033[1;32;1m Executing Mission 3 ... \033[0m\n")

df = pd.DataFrame(codeStatus)
df.to_csv(f"stockList_{str_endDate}.csv", index=False)
# df.to_excel(f"stockList_{str_endDate}.xlsx", index=False)     // If you want to save as excel


print(f"Number of stock access: {count}")
print(f"Number of error encounter while scraping: {len(errorCount)}")
print(errorCount)    
                                                                                  

print("\033[1;32;1m Mission 3 Complete ! \033[0m\n")
print("\033[1;32;1m Finish !!! \033[0m\n")

# --------------------------------------------------------------------------------------------------

"""
CREATE TABLE StockObservation (
    id INT PRIMARY KEY AUTO INCREMENT,
    Date TIMESTAMP, 
    OpenPrice DOUBLE,
    ClosePrice DOUBLE,
    VOLUME INT
)

SELECT * FROM StockObservation WHERE ....
"""
