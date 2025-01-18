from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from predictive_model import load_model, predict_delivery_time
from route_optimization import optimize_route, vehicle_routing
from data_scraping import fetch_traffic_data, fetch_weather_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logistics_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_location = db.Column(db.String(128), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    order_priority = db.Column(db.Integer, nullable=False)
    traffic_level = db.Column(db.Float, nullable=False)
    weather_conditions = db.Column(db.Float, nullable=False)
    delivery_time = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(64), nullable=False, default='pending')

@app.route('/predict_delivery_time', methods=['POST'])
def predict():
    data = request.json
    model = load_model()
    delivery_time = predict_delivery_time(model, data)
    return jsonify({"predicted_delivery_time": delivery_time})

@app.route('/optimize_route', methods=['POST'])
def optimize():
    locations = request.json.get('locations', [])
    path, distance = optimize_route(locations)
    return jsonify({"path": path, "distance": distance})

@app.route('/optimize_allocation', methods=['POST'])
def optimize_allocation():
    results = vehicle_routing()
    return jsonify({"solution": results})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
