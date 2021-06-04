from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import requests
import time
from selenium.webdriver.common.keys import Keys

class Stock_scraping:
    def __init__(self):

        # No windows will occur
        global options
        options = webdriver.FirefoxOptions()
        options.set_headless(headless=True)
        assert options.headless
        num = int(input("How many stocks you want to find?:    "))
        self.stocks_list = [input("enter your stock:   ") for i in range(num)]
        self.type_list = ["Candle", "Bar", "Mountain", "Line", "OHLC", "HLC"]
        self.data_image = []
        print(f"Stocks you are looking for: {self.stocks_list}")
        print("Receive your command, now processing")

    def yahoo_stock(self):
        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
        url = "https://hk.finance.yahoo.com/"
        browser.get(url)

        for stock in self.stocks_list:
            search_bar = browser.find_element_by_id("yfin-usr-qry")
            search_bar.click()
            search_bar.send_keys(stock)
            search_bar.send_keys(Keys.ENTER)
            time.sleep(3)

            # inline tab to click on
            tablists = browser.find_elements_by_xpath(
                "//a[@class='Lh(44px) Ta(c) Bdbw(3px) Bdbs(s) Px(12px) C($linkColor) Bdbc($seperatorColor) D(b) Td(n) selected_Bdbc($linkColor) selected_C($primaryColor) selected_Fw(b) ']")
            for tab in tablists:
                if "chart" in tab.get_attribute("href"):
                    tab.click()

            # chart we want to obtain
            # Not solute yet
            charts = browser.find_elements_by_xpath("//div[@class='stx-holder stx-panel-chart']")
            print(charts)
            time.sleep(4)

    def AA_stocks(self):
        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
        url = "http://www.aastocks.com/en/usq/default.aspx"
        browser.get(url)

        for i, x in enumerate(self.stocks_list):
            self.data_image.append([])
            search_bar = browser.find_element_by_xpath("//input [@id='sb-txtSymbol-aa']")
            search_bar.click()
            search_bar.send_keys(self.stocks_list[i])
            search_bar.send_keys(Keys.ENTER)
            time.sleep(2)

            # Technical Analysis Page
            browser.find_element_by_xpath("//div [@class='tab-middle  tab-middle-half']").click()

            # 1) Candle Image
            browser.find_element_by_xpath('//div [@id="ctbChartType_1"]').click()
            img = browser.find_element_by_xpath('//img [@id="cp_ChartImg"]').get_attribute("src")
            self.data_image[i].append(img)
            time.sleep(2)

            # 2) Bar Image
            browser.find_element_by_xpath('//div [@id="ctbChartType_4"]').click()
            img = browser.find_element_by_xpath('//img [@id="cp_ChartImg"]').get_attribute("src")
            self.data_image[i].append(img)
            time.sleep(2)

            # 3) Mountain
            browser.find_element_by_xpath('//div [@id="ctbChartType_6"]').click()
            img = browser.find_element_by_xpath('//img [@id="cp_ChartImg"]').get_attribute("src")
            self.data_image[i].append(img)
            time.sleep(2)

            # 4) Line
            browser.find_element_by_xpath('//div [@id="ctbChartType_5"]').click()
            img = browser.find_element_by_xpath('//img [@id="cp_ChartImg"]').get_attribute("src")
            self.data_image[i].append(img)
            time.sleep(2)

            # 5) OHLC
            browser.find_element_by_xpath('//div [@id="ctbChartType_2"]').click()
            img = browser.find_element_by_xpath('//img [@id="cp_ChartImg"]').get_attribute("src")
            self.data_image[i].append(img)
            time.sleep(2)

            # 6) HLC
            browser.find_element_by_xpath('//div [@id="ctbChartType_3"]').click()
            img = browser.find_element_by_xpath('//img [@id="cp_ChartImg"]').get_attribute("src")
            self.data_image[i].append(img)
            time.sleep(2)

            for a in range(len(self.data_image)):
                r = requests.get(self.data_image[i][a], stream=True)
                time.sleep(5)
                filename = "D://Python_Stock_Data/" + str(self.stocks_list[i]) + "  " +  str(self.type_list[i]) + ".gif"
                print(f"downloading ... {self.stocks_list[i]} {self.type_list[i]}")
                with open (filename, "wb") as f:
                    for chunk in r:
                        f.write(chunk)
                        time.sleep(5)

    def data_sources(self):
        print("1. Yahoo Financial, 2. AA stocks...")
        source = input("Please choose one the stock webs in number")
        if source == "1":
            self.yahoo_stock()
        elif source == "2":
            self.AA_stocks()
        else:
            print("sorry! I don't understand")
            quit()

a = Stock_scraping()
a.data_sources()