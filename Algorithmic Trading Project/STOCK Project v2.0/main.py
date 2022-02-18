"""
Logic:

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

# 4. DataBase
import mysql.connector
import SQLconnectSret as secret
import pandas as pd
from sqlalchemy import Column, String, create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData



#-------------------------------          Part 1: Scrap Stock Code    -------------------------------------

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




#-------------------------------          Part 2: Scrap Stock Price    -------------------------------------


count = 0                                          # successful searching
errorCount = 0                                     # fail searching

endDate = datetime.now()                           # Current time system (your computer)
startDate = endDate - timedelta(days=1)            # Two days before current (your computer)

str_endDate = endDate.strftime("%Y-%m-%d")         # date obj. to string   
str_startDate = startDate.strftime("%Y-%m-%d")     
errorCode = []                                     # append to list

codeStatus = {                                     # Open, close, and volume
    "Code": [],
    "Date": [],
    "Open ($)": [],
    "Close ($)": [],
    "Volume": [],
    "Percentage Change": []
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
    
            codeStatus["Code"].append(code)
            codeStatus["Date"].append(stockDate)
            codeStatus["Open"].append(stockOpen)
            codeStatus["Close"].append(stockClose)
            codeStatus["Volume"].append(stockVolume)

            # Be later calculated in database
            codeStatus["Percentage Change"].append(0)


        
        print(f" Successful: {code}")
          
    except:
        print(f"\033[1;31m Has probelems on -----{code} \033[0m")          # red color for fail 
        errorCode.append(code)
        
        
print("\033[1;32;1m Mission 2 Complete ! \033[0m\n")


#----------------------------  Part 3: Data Merging and export to Database      ----------------------------------

print("\033[1;32;1m Executing Mission 3 ... \033[0m\n")

df = pd.DataFrame(codeStatus)


"""Set up database"""
mysql.connector.connect()
conn = mysql.connector.connect(host = secret.host, user = secret.user, password = secret.password)
mycur = conn.cursor()
database_ = "STOCKDB"
mycur.execute("""CREATE DATABASE IF NOT EXISTS """ + database_)
conn.close()


""" Append dataframe into database"""
conn = mysql.connector.connect(host = secret.host, user = secret.user, password = secret.password, database = database_, port = secret.port)
engine = create_engine("mysql+mysqlconnector://" + secret.user + ":" + secret.password + "@" + secret.host + "/" + database_)


# Create Table via sqlalchemy
meta = MetaData()
Table(
   'stockTransaction', meta, 
   Column('id', Integer, primary_key = True), 
   Column('Code', String(2000)), 
   Column('Date', String(2000)), 
   Column('Open ($)', String(2000)),
   Column('Close ($)', String(2000)),
   Column('Volume', Integer),
   Column('Percentage Change', Integer)
)
meta.create_all(engine)


# Append data into Database
df.to_sql(con=engine, name="stocktransaction", if_exists="append", index=False)
                                                                           
print("\033[1;32;1m Mission 3 Complete ! \033[0m\n")



#----------------------------  Part 4: Database Calculation (Price % change && Keep / Drop decision)    ----------------------------------


# Create New Table to Store Stock and Status
"""  
CREATE TABLE StockCode AS 
		(SELECT  
			Stock code, 
			CASE  Status WHEN PerChange > =10 
				THEN 
					Status = 'K'
				ELSE  'D'
			END
		FROM Transaction;)
"""

Table(
   'stockcode', meta, 
   Column('Code', String(2000)),  
   Column('Code Status', String(40))
)
meta.create_all(engine)


print("\033[1;32;1m Finish !!! \033[0m\n")