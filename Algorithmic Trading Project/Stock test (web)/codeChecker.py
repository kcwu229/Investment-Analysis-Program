# 1. Scraping  Teams
import requests
from bs4 import BeautifulSoup
import string
import re

def StockChecker(stockLetter):
    codes = []        
    if (stockLetter == 'All'):
        stockLetter = list(string.ascii_uppercase)
        
    for letter in stockLetter:
        url = f"https://eoddata.com/stocklist/NASDAQ/{letter}.htm"          # Capital A-Z according to web's pattern
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'lxml')                           # turn into DOM structure
            
        # filter with special pattern: stockquote/NASDAQ/...
        tags = soup.find_all("a", href=re.compile("/stockquote/NASDAQ/"))   # regular expression for specified searching 
        codes = [code.string for code in tags if code.string != None]
                            
    # Return the code lists
    return codes
