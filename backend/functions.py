import matplotlib
matplotlib.use('GTK3Agg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
import pandas as pd


def allowed_file(filename):
    ALLOWED_EXTENSIONS = ['xls', 'csv']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Linear Regression data
def linear_regression(csv_file):
    df = pd.read_csv(csv_file)
    print(df)
    Y = df['prices']
    X = df['month']

    X = X.values.reshape(len(X), 1)
    Y = Y.values.reshape(len(Y), 1)

    # Segmenting the data into training and test subsets
    X_train = X[:-250]
    X_test = X[-250:]

    Y_train = Y[:-250]
    Y_test = Y[-250:]

    plt.scatter(X_test, Y_test, color='black')
    plt.title('Price Regression')
    plt.xlabel('Date')
    plt.ylabel('Prices')
    plt.xticks(())
    plt.yticks(())
    # Initializing the linear regression model
    #regr = linear_model.LinearRegression()

    # Training the model using the training subset
    #regr.fit(X_train, Y_train)
    # plt.plot(X_test, regr.predict(X_test), color='red', linewidth=3)
    return plt.show()