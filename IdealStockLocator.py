from Stock import Stock
from Data import Data
import statistics as stat
import pandas as pd


class IdealStockLocator:
    symbols = []
    ideal_stocks = []

    # Analyze what stocks will be ideal for building models
    # Parameters:
    #   symbols - the set of symbols that will analyzed (default is sp500)
    def __init__(self, symbols=None):
        if symbols is not None:
            self.custom_symbols(symbols)
        else:
            self.sp500_symbols()

        self.find_ideal_stocks()

        self.write_to_file()

        print(str(len(self.ideal_stocks)) + " of " + str(len(self.symbols)) + " are ideal stocks")

    def custom_symbols(self, symbols):
        self.symbols = symbols

    # Pull the symbols of the stocks in the S and P 500
    def sp500_symbols(self):
        data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        table = data[0]
        sliced_table = table[1:]
        header = table.iloc[0]
        corrected_table = sliced_table.rename(columns=header)
        self.symbols = corrected_table.iloc[:, 0].tolist()

    # Locate the stocks that are ideal for building models
    # Ideal stocks are defined as stocks that are sampled and have a std dev gain that is smaller than their mean gain
    # Parameters:
    #   samples - the number of samples taken of each stock
    #   standard - the minimum difference between mean and stddev to make a stock ideal
    def find_ideal_stocks(self, samples=50, standard=0.000000000000000001):
        for symbol in self.symbols:
            print("Analyzing " + symbol + "...")
            gain = []
            try:
                data = Data(symbol)
                for i in range(samples):
                    stock = Stock(symbol, data)
                    gain.append(stock.get_score()["gain"])
                    data.partition()

                mean = stat.mean(gain)
                stddev = stat.stdev(gain)

                if mean - stddev > standard:
                    self.ideal_stocks.append(symbol)
            except:
                print(symbol + " IGNORED!")

    # Get the ideal stocks
    def get_ideal_stocks(self):
        return self.ideal_stocks

    # Write the ideal stocks into a text file
    def write_to_file(self):
        f = open("idealStocks.txt", "w")
        for stock in self.ideal_stocks:
            f.write(stock + "\n")
        f.close()
