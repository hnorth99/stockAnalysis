from sklearn import tree
import pandas as pd

class Stock:
    symbol = None
    data = None
    clf = None
    result = {"opportunities": None,
              "gain": None,
              "reach": None,
              "safety": None}

    def __init__(self, symbol, data):
        # create stock ticker/object
        self.symbol = symbol

        # pull and format data
        self.data = data

        # train model
        self.train_model()

        # test model
        self.test_model()

    # Train the model
    def train_model(self):
        # break data into training cols and target cols
        x_train = self.data.get_x_train()
        y_train = self.data.get_y_train()

        # build model
        self.clf = tree.DecisionTreeClassifier()
        self.clf.fit(x_train, y_train)

    # Test the model
    def test_model(self):
        # get testing data
        x_test = self.data.get_x_test()
        y_test = self.data.get_y_test()
        # make predictions
        prediction = self.clf.predict(x_test)

        # set base price
        base_price = x_test.iloc[0, x_test.shape[1] - 1]

        # check predictions and calculate the success of our model
        spend = 0.
        sell = 0.
        transaction = 0.
        success = 0.
        for i in range(prediction.shape[0] - 1):
            if prediction[i] > 0:
                spend += x_test.iloc[i, x_test.shape[1] - 1]
                sell += x_test.iloc[i + 1, x_test.shape[1] - 1]
                transaction += 1

                if y_test[i] > 0:
                    success += 1

        # store model scores
        self.result["opportunities"] = prediction.shape[0]
        self.result["gain"] = (sell - spend) / base_price
        self.result["reach"] = transaction / prediction.shape[0]
        if transaction > 0:
            self.result["safety"] = success / transaction
        else:
            self.result["safety"] = -1

    # Get the models score
    def get_score(self):
        return self.result

    # Print an overview of the stock (symbol name and model scores)
    def print_overview(self):
        print(self.symbol)
        self.print_score()
        print("")

    # Print the scores of the stock
    def print_score(self):
        print("opportunities = " + str(self.result["opportunities"]))
        print("gain = " + str(self.result["gain"]))
        print("reach = " + str(self.result["reach"]))
        print("safety = " + str(self.result["safety"]))