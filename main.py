from IdealStockLocator import IdealStockLocator
from FinalModelCreator import FinalModelCreator
from Data import Data
from Stock import Stock

import time

def main():
    t0 = time.time()

    ideal_stock_locator = IdealStockLocator()
    final_models = FinalModelCreator()

    t1 = time.time()
    print(str(t1 - t0) + " to execute")

def specific():
    t0 = time.time()

    ideal_stock_locator = IdealStockLocator(["AMZN", "GOOGL"])
    final_models = FinalModelCreator()

    t1 = time.time()
    print(str(t1 - t0) + " to execute")

def dataTesting():
    data = Data("AMZN")
    data.show_data()

def stockTesting():
    data = Data("AAPL")
    aapl = Stock("AAPL", data)
    aapl.print_overview()

if __name__ == '__main__':
    #main()
    #specific()
    #dataTesting()
    stockTesting()
