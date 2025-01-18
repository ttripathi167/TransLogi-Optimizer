# Fully Functional Python Code for the use the create the dashbaorad 

import streamlit as st
import folium
from streamlit_folium import st_folium
import os
import pickle
import numpy as np
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sklearn.linear_model import LinearRegression
import networkx as nx
from pulp import LpProblem, LpVariable, LpMinimize
import threading
import requests
import datetime
import docker

# Flask Setup
app = Flask(_name_)
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

# API Keys
TRAFFIC_API_KEY = 'your_traffic_api_key'
WEATHER_API_KEY = 'your_weather_api_key'

# Helper Functions for Data Collection
import requests

def fetch_traffic_data(location):
    try:
        # Replace with the actual traffic API URL
        url = f'https://maps.googleapis.com/maps/api/traffic_data?location={location}&key={TRAFFIC_API_KEY}'
        response = requests.get(url)
        
        # Check if the response status code is 200 (OK)
        response.raise_for_status()
        
        # Check if the response content is empty
        if not response.text:
            print(f"Error: Empty response for location {location}")
            return 0  # Return a default value
        
        # Try to parse the JSON response
        data = response.json()
        
        # Check if the expected 'traffic_level' field is in the response
        if 'traffic_level' in data:
            return data['traffic_level']
        else:
            print(f"Error: 'traffic_level' not found in response for location {location}")
            return 0  # Return a default value if 'traffic_level' is missing
            
    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors (e.g., 404, 500)
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        # Handle general request errors (e.g., network issues)
        print(f"Request error occurred: {req_err}")
    except ValueError as json_err:
        # Handle JSON parsing errors
        print(f"JSON error occurred: {json_err}")
    except Exception as e:
        # Catch any other exceptions
        print(f"An unexpected error occurred: {e}")
    
    # Return a default value in case of any error
    return 0

def fetch_weather_data(location):
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}')
    if response.status_code == 200:
        weather = response.json()
        return weather['main']['humidity']
    else:
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
    priority = st.slider("Order Priority", 1, 25)
    
    # Add the submit button inside the form
    submit_button = st.form_submit_button(label="Submit Order")

    # Ensure the button's action is wrapped properly
    if submit_button:
        if order_id and customer_location:
            traffic = fetch_traffic_data(customer_location)
            weather = fetch_weather_data(customer_location)
            
            st.success("Order submitted successfully!")
            model = load_model()
            predicted_time = predict_delivery_time(model, {
                'distance': distance,
                'order_priority': priority,
                'traffic_level': traffic,
                'weather_conditions': weather
            })
            st.write(f"Predicted Delivery Time: {predicted_time:.2f} hours")
        else:
            st.error("Please fill in all the fields before submitting.")

# Run Flask in a Thread
if __name__ == "__main__":
    threading.Thread(target=start_flask).start()

# Run the code On the VS Code Terminal Use the following Command to execute the whole code
1) pip install --upgrade flask-sqlalchemy Flask Werkzeug scikit-learn streamlit folium streamlit-folium networkx pulp psycopg2-binary requests
2) streamlit run translogi_system.py
