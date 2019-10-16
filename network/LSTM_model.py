import tensorflow as tf
import numpy as np
import pandas
import yfinance as fix

from preprocessing import DataProcessing

fix.pdr_override()

keras = tf.keras
K = keras.backend
KL = keras.layers

def main():
    process = DataProcessing("sales.csv", 0.9)
    process.gen_test(10)
    process.gen_train(10)

    X_train = process.X_train.reshape((239, 10, 1)) / 200
    Y_train = process.Y_train / 200

    X_test = process.X_test.reshape(9, 10, 1) / 200
    Y_test = process.Y_test / 200

    model = tf.keras.Sequential()
    model.add(KL.LSTM(20, input_shape=(10, 1), return_sequences=True))
    model.add(KL.LSTM(20))
    model.add(KL.Dense(1, activation=tf.nn.relu))

    model.compile(optimizer="adam", loss="mean_squared_error")
    model.fit(X_train, Y_train, epochs=50)
    print(model.evaluate(X_test, Y_test))

    data = pandas.read_csv('sales_with_header.csv', sep=',').sample(n=10)
    stock = data["Price"]
    X_predict = np.array(stock).reshape((1, 10, 1)) / 200
    print(model.predict(X_predict) * 200)

    # If instead of a full backtest, you just want to see how accurate the model is for a particular prediction, run this:
    # data = pdr.get_data_yahoo("AAPL", "2017-12-19", "2018-01-03")
    # stock = data["Adj Close"]
    # X_predict = np.array(stock).reshape((1, 10)) / 200
    # print(model.predict(X_predict)*200)

if __name__ == '__main__':
    main()

