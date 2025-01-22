from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from predictive_model import load_model, predict_delivery_time
from services.route_optimization import optimize_route, vehicle_routing  # Correct import
from data_scraping import fetch_traffic_data, fetch_weather_data

# Initialize Flask app
app = Flask(__name__)

# Configure database (ensure correct URI is provided)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Trisha@localhost:5433/TransLogi_DB'  # Change to your actual DB URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)

# 🚀 Add root endpoint
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
    # Ensure the database exists and is created within the app context
    with app.app_context():
        # Ensure the database is created
        db.create_all()
        print("✅ Database initialized!")

    # Run the Flask app
    app.run(debug=True, host="127.0.0.1", port=5000)
