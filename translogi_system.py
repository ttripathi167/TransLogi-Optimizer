# translogi_system.py
import streamlit as st
import folium
from streamlit_folium import st_folium
import os
import pickle
import numpy as np
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sklearn.linear_model import LinearRegression
import networkx as nx
from pulp import LpProblem, LpVariable, LpMinimize
import threading
import requests

# Flask Setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logistics_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_location = db.Column(db.String(128), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    order_priority = db.Column(db.Integer, nullable=False)
    traffic_level = db.Column(db.Float, nullable=False)
    weather_conditions = db.Column(db.Float, nullable=False)
    delivery_time = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(64), nullable=False, default='pending')

# API Keys (You should replace these with actual keys)
TRAFFIC_API_KEY = 'your_traffic_api_key'
WEATHER_API_KEY = 'your_weather_api_key'

# Helper Functions for Data Collection
def fetch_traffic_data(location):
    try:
        url = f'https://maps.googleapis.com/maps/api/traffic_data?location={location}&key={TRAFFIC_API_KEY}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('traffic_level', 0)
    except Exception as e:
        print(f"Error fetching traffic data: {e}")
        return 0

def fetch_weather_data(location):
    try:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}'
        response = requests.get(url)
        response.raise_for_status()
        weather = response.json()
        return weather['main'].get('humidity', 0)
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return 0

# Machine Learning Model
MODEL_PATH = 'logistics_model.pkl'

def load_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as file:
            return pickle.load(file)
    else:
        return train_model()

def train_model():
    X = np.random.rand(100, 4)
    y = X[:, 0] * 2 + X[:, 1] * 3 + X[:, 2] * 1.5 + X[:, 3] * 0.5
    model = LinearRegression().fit(X, y)
    with open(MODEL_PATH, 'wb') as file:
        pickle.dump(model, file)
    return model

def predict_delivery_time(model, data):
    features = np.array([data['distance'], data['order_priority'], data['traffic_level'], data['weather_conditions']]).reshape(1, -1)
    return model.predict(features)[0]

# Route Optimization
def optimize_route(locations):
    G = nx.Graph()
    for loc in locations:
        G.add_edge(loc[0], loc[1], weight=loc[2])
    source, destination = locations[0][0], locations[-1][1]
    path = nx.shortest_path(G, source=source, target=destination, weight='weight')
    distance = nx.shortest_path_length(G, source=source, target=destination, weight='weight')
    return path, distance

def vehicle_routing():
    problem = LpProblem("VehicleRouting", LpMinimize)
    x1 = LpVariable("Route1", 0, 1, cat="Binary")
    x2 = LpVariable("Route2", 0, 1, cat="Binary")
    problem += 10 * x1 + 15 * x2, "Minimize Costs"
    problem += x1 + x2 == 1, "One route must be selected"
    problem.solve()
    return {var.name: var.varValue for var in problem.variables()}

# Flask Routes
@app.route('/predict_delivery_time', methods=['POST'])
def predict():
    data = request.json
    if not all(key in data for key in ['distance', 'order_priority', 'traffic_level', 'weather_conditions']):
        return jsonify({"message": "Invalid input!"}), 400

    model = load_model()
    delivery_time = predict_delivery_time(model, data)
    return jsonify({"predicted_delivery_time": delivery_time})

@app.route('/optimize_route', methods=['POST'])
def optimize():
    data = request.json
    if 'locations' not in data:
        return jsonify({"message": "Invalid input!"}), 400

    locations = data['locations']
    path, distance = optimize_route(locations)
    return jsonify({"path": path, "distance": distance})

@app.route('/optimize_allocation', methods=['POST'])
def optimize_allocation():
    results = vehicle_routing()
    return jsonify({"solution": results})

# Start Flask App in a Separate Thread
def start_flask():
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader=False)

# Streamlit Setup
st.set_page_config(page_title="Logistics Dashboard", layout="wide")
st.title("Logistics Dashboard")
st.write("""
Welcome to the Logistics Dashboard! Visualize delivery locations, predict delivery times, and optimize logistics routes.
""")

# Map Section
st.header("Delivery Map")
start_coords = (37.7749, -122.4194)
map_object = folium.Map(location=start_coords, zoom_start=13)
folium.Marker(location=start_coords, popup="Start Location").add_to(map_object)
st_folium(map_object, width=700, height=500)

# Order Submission Form
st.header("Submit a New Order")
with st.form("order_form"):
    order_id = st.text_input("Order ID", placeholder="Enter Order ID")
    customer_location = st.text_input("Customer Location", placeholder="Enter Customer Location")
    distance = st.number_input("Distance (km)", min_value=0.0, step=0.1)
   
