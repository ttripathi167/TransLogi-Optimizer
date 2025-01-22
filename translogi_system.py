from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json

# Initialize Flask app and SQLAlchemy
app = Flask(__name__)

# Configure database (PostgreSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Trisha@localhost:5433/TransLogi_DB'  # Update credentials here
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the models (table structures)
class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    optimized_route = db.Column(db.JSON, nullable=True)  # Stores the optimized route as JSON

class UserInput(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_data = db.Column(db.JSON, nullable=False)  # Stores dashboard inputs as JSON
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())  # Auto-generates timestamp

# Create the database tables
with app.app_context():
    db.create_all()

# API endpoint to retrieve all routes
@app.route('/api/routes', methods=['GET'])
def get_routes():
    routes = Route.query.all()  # Query all routes from the database
    return jsonify([{
        'id': route.id,
        'source': route.source,
        'destination': route.destination,
        'distance': route.distance,
        'optimized_route': route.optimized_route
    } for route in routes])  # Return routes in JSON format

# API endpoint to add a new route
@app.route('/api/routes', methods=['POST'])
def add_route():
    data = request.json
    try:
        # Create a new Route entry
        new_route = Route(
            source=data['source'],
            destination=data['destination'],
            distance=data['distance'],
            optimized_route=data.get('optimized_route')
        )
        db.session.add(new_route)
        db.session.commit()
        return jsonify({'message': 'Route added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to retrieve user inputs
@app.route('/api/user_inputs', methods=['GET'])
def get_user_inputs():
    inputs = UserInput.query.all()  # Query all user inputs from the database
    return jsonify([{
        'id': user_input.id,
        'input_data': user_input.input_data,
        'timestamp': user_input.timestamp
    } for user_input in inputs])  # Return inputs in JSON format

# API endpoint to add user inputs from the dashboard
@app.route('/api/user_inputs', methods=['POST'])
def add_user_input():
    data = request.json
    try:
        # Create a new UserInput entry
        new_input = UserInput(input_data=data)
        db.session.add(new_input)
        db.session.commit()
        return jsonify({'message': 'User input added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Example integrated logic: retrieve optimized routes and user inputs together
@app.route('/api/overview', methods=['GET'])
def get_overview():
    try:
        # Fetch routes and user inputs
        routes = Route.query.all()
        user_inputs = UserInput.query.all()

        # Combine data into a single response
        data = {
            'routes': [{
                'id': route.id,
                'source': route.source,
                'destination': route.destination,
                'distance': route.distance,
                'optimized_route': route.optimized_route
            } for route in routes],
            'user_inputs': [{
                'id': user_input.id,
                'input_data': user_input.input_data,
                'timestamp': user_input.timestamp
            } for user_input in user_inputs]
        }
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Script to add sample data to the database
@app.route('/api/seed_data', methods=['POST'])
def seed_data():
    try:
        routes = [
            Route(source="New York", destination="Los Angeles", distance=2800, optimized_route={"route": "NY -> LA"}),
            Route(source="Chicago", destination="Houston", distance=1080, optimized_route={"route": "CHI -> HOU"})
        ]
        db.session.bulk_save_objects(routes)
        db.session.commit()
        return jsonify({'message': 'Sample data added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)


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

# Root endpoint
@app.route('/', methods=['GET'])
def home():
    return "🚀 API is running on http://127.0.0.1:5000!"

if __name__ == '__main__':
    app.run(debug=True)
