from Data import Data
from Stock import Stock
import numpy as np


class FinalModelCreator:
    idealStocks = None
    models = {}

    def __init__(self):
        self.open_ideal_stocks()
        self.create_final_models()

        for model in self.models.values():
            model.print_overview()

    # Read in the ideal stocks from the text file edited by IdealStockLocator class
    def open_ideal_stocks(self):
        f = open("idealStocks.txt", "r")
        self.idealStocks = f.readlines()
        f.close()

    # Create the final models for all the ideal stocks
    def create_final_models(self):
        for symbol in self.idealStocks:
            symbol = symbol.strip()
            print("Creating model for " + symbol + "...")
            sample_models = []
            gains = []
            data = Data(symbol)

            for i in range(5):
                data.partition()
                sample_stock = Stock(symbol, data)
                sample_models.append(sample_stock)
                gains.append(sample_stock.get_score()["gain"])

            median = np.argsort(gains)[len(gains) // 2]
            self.models[symbol] = sample_models[median]

    # Return the final models created
    def get_final_models(self):
        return self.models