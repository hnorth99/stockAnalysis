import yfinance as yf
import numpy as np
import pandas as pd

class Data:
    full_data = None
    training_indices = None
    predictor_columns = []
    target_columns = None

    def __init__(self, symbol, period="6mo"):
        # pull data from yahoo finance over the previous (period)
        ticker = yf.Ticker(symbol)
        self.full_data = ticker.history(period)

        self.format_data()
        self.feature_engineering()

        self.partition()

    # Drop useless rows and address other structural issues
    def format_data(self):
        # drop useless cols
        self.full_data = self.full_data.drop(["Dividends", "Stock Splits"], axis=1)

    # Create new custom columns and add them to data
    def feature_engineering(self):
        # create target col
        self.add_forward_column("One Day Forward (OtoO)", "Open", "Open", 1)
        self.target_columns = "One Day Forward (OtoO)"

        # create predictor cols
        for i in range(1, 3):
            # OtoO
            self.add_backward_column(str(i) + " Day Back (OtoO)", "Open", "Open", i)
            self.predictor_columns.append(str(i) + " Day Back (OtoO)")
            # VtoV
            self.add_backward_column(str(i) + " Day Back (VtoV)", "Volume", "Volume", i)
            self.predictor_columns.append(str(i) + " Day Back (VtoV)")

        # add open price to predictor cols
        self.predictor_columns.append("Open")

    # Add a col that uses forward computational math
    # DEPENDENT ON FUTURE - NO PREDICTOR COLS ONLY TARGET
    # Parameters:
    #   name - the name of the new col
    #   column_a - name of col for feature engineering (column_a is base)
    #   column_b - name of col for feature engineering (column_b is future)
    #   span - number of days separating difference between column_a and column_b
    def add_forward_column(self, name, column_a, column_b, span, percent_round = True):
        new_column = []

        # add data to empty array
        for i in range(self.full_data.shape[0] - span):
            value = self.full_data.iloc[i + span][column_b] - self.full_data.iloc[i][column_a]
            value = value / self.full_data.iloc[i][column_a] * 100
            if percent_round:
                value = int(value)
            new_column.append(value)

        # add dummy placeholder for futures
        for i in range(span):
            new_column.append(0)  # MAYBE CHANGE TO NONE FOR FUTURE ML TRAINING

        self.full_data[name] = new_column

    # Add a col that uses backward computational math
    # DEPENDENT ON PAST - NO TARGET COLS ONLY PREDICTORS
    # Parameters:
    #   name - the name of the new col
    #   column_a - name of col for feature engineering (column_a is base)
    #   column_b - name of col for feature engineering (column_b is past)
    #   span - number of days separating difference between column_a and column_b
    def add_backward_column(self, name, column_a, column_b, span):
        new_column = []

        # add dummy placeholder for futures
        for i in range(span):
            new_column.append(0)  # MAYBE CHANGE TO NONE FOR FUTURE ML TRAINING

        # add data to empty array
        for i in range(self.full_data.shape[0] - span):
            value = self.full_data.iloc[i + span][column_a] - self.full_data.iloc[i][column_b]
            value = value / self.full_data.iloc[i][column_b]
            new_column.append(value)

        self.full_data[name] = new_column

    # Determine the indices that will be used to partition the data into training and testing sets
    # Parameters:
    #   training_size - the percentage of data that will make be used in the training set
    def partition(self, training_size=0.8):
        msk = np.random.rand(len(self.full_data)) < training_size
        self.training_indices = msk

    # Get the training data
    def get_training_data(self):
        return self.full_data[self.training_indices]

    # Get the testing data
    def get_testing_data(self):
        return self.full_data[~self.training_indices]

    # Get the predictors for the training data
    def get_x_train(self):
        return self.get_training_data()[self.predictor_columns]

    # Get the target for the training data
    def get_y_train(self):
        return self.get_training_data()[self.target_columns]

    # Get the predictors for the testing data
    def get_x_test(self):
        return self.get_testing_data()[self.predictor_columns]

    # Get the target for the testing data
    def get_y_test(self):
        return self.get_testing_data()[self.target_columns]

    # Print out the predictor testing data
    def show_data(self):
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)
        print(self.full_data)
