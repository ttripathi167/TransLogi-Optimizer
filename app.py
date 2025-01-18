from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# Import custom modules (Ensure these exist)
try:
    from predictive_model import load_model, predict_delivery_time
    from route_optimization import optimize_route, vehicle_routing
    from data_scraping import fetch_traffic_data, fetch_weather_data
except ImportError:
    print("⚠️ Missing module(s): Ensure predictive_model, route_optimization, and data_scraping exist!")

# Initialize Flask app
app = Flask(__name__)

# Configure database
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logistics_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_location = db.Column(db.String(128), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    order_priority = db.Column(db.Integer, nullable=False)
    traffic_level = db.Column(db.Float, nullable=False)
    weather_conditions = db.Column(db.Float, nullable=False)
    delivery_time = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(64), nullable=False, default='pending')

# 🚀 ADD ROOT ENDPOINT TO FIX 404 ERROR
@app.route('/', methods=['GET'])
def home():
    return "🚀 API is running on http://127.0.0.1:5000!"

@app.route('/predict_delivery_time', methods=['POST'])
def predict():
    data = request.json
    try:
        model = load_model()
        delivery_time = predict_delivery_time(model, data)
        return jsonify({"predicted_delivery_time": delivery_time})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/optimize_route', methods=['POST'])
def optimize():
    locations = request.json.get('locations', [])
    if not locations:
        return jsonify({"error": "Missing locations parameter"}), 400

    try:
        path, distance = optimize_route(locations)
        return jsonify({"path": path, "distance": distance})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/optimize_allocation', methods=['POST'])
def optimize_allocation():
    try:
        results = vehicle_routing()
        return jsonify({"solution": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Ensure the database exists
    if not os.path.exists("logistics_system.db"):
        with app.app_context():
            db.create_all()
        print("✅ Database initialized!")
    else:
        print("✅ Database already exists!")

    app.run(debug=True, host="127.0.0.1", port=5000)
