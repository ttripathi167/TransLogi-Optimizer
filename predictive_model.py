import os
import pickle
import numpy as np
from sklearn.linear_model import LinearRegression

MODEL_PATH = 'logistics_model.pkl'

def train_model():
    X = np.random.rand(100, 4)
    y = X[:, 0] * 2 + X[:, 1] * 3 + X[:, 2] * 1.5 + X[:, 3] * 0.5
    model = LinearRegression().fit(X, y)
    with open(MODEL_PATH, 'wb') as file:
        pickle.dump(model, file)
    return model

def load_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as file:
            return pickle.load(file)
    else:
        return train_model()

def predict_delivery_time(model, data):
    features = np.array([data['distance'], data['order_priority'], data['traffic_level'], data['weather_conditions']]).reshape(1, -1)
    return model.predict(features)[0]
