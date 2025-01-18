# USER GUIDE
Welcome to the Logistics System web application! This guide provides detailed information about the project files and how to use the application effectively.

# Project Overview
The application helps users manage logistics, including:

* Adding orders
* Viewing optimized delivery routes
* Predicting delivery times
* Interpreting dashboard metrics and visualizations
  
## File Structure
**Core Application Files**

* data_scraping.py
- Functionality: Scrapes data from various logistics sources, including APIs and web pages, and stores it in a structured format.
- Usage: Automatically updates datasets for predictions and analytics.
 
* predictive_model.py
- Functionality: Contains machine learning models to predict delivery times based on historical and live data.
- Usage: Powers the prediction feature in the web application.

* route_optimization.py
- Functionality: Provides route optimization logic using advanced algorithms such as Dijkstra’s or linear programming.
- Usage: Generates optimized routes for efficient deliveries.
  
* app.py
- Functionality: Main Flask application file serving the API for data entry, user authentication, and backend logic.
- Usage: Runs the server for the application backend.
  
* dashboard.py
- Functionality: Streamlit application that provides a user-friendly dashboard for metrics and visualizations.
- Usage: Displays interactive visualizations and analytics for users.
  
# Containerization Files

* Dockerfile
- Functionality: Defines the environment for the application, including dependencies and ports.
- Usage: Used to build Docker containers.
  
* docker-compose.yml
- Functionality: Orchestrates multiple services (e.g., Flask API, PostgreSQL, Streamlit dashboard).
- Usage: Runs the entire application in a containerized environment.
  
# Configuration Files

* requirements.txt
- Functionality: Lists all Python dependencies required by the application.
- Usage: Installed during the Docker build process.
  
* Database (PostgreSQL)
-Integrated with the system using docker-compose.yml for seamless data storage and retrieval.

# How to Use the Web Application

**1. Log In or Sign Up**
- Navigate to the homepage.
- Sign Up: Provide your email and password to create an account.
- Log In: Use your credentials to access the application.
  
**2. Add Orders**
- Access the "Orders" section of the application.
- Enter order details, including pickup and delivery addresses, package weight, and any special instructions.
- Submit the form to add the order to the database.
  
**3. View Maps**
- Navigate to the "Routes" section.
- View a map showing the current orders, delivery locations, and optimized routes.
- Use filters to customize the view (e.g., date range, delivery zones).
  
**4. Predict Delivery Times**
- Access the "Predictions" feature.
- Select an order or provide the required details (e.g., pickup and delivery locations, weight).
- View the estimated delivery time based on the predictive model.
  
**5. Optimize Routes**
- Go to the "Optimization" section.
- Select the orders for optimization.
- The system will calculate and display the most efficient route, saving time and resources.
  
**6. Interpret Dashboard Metrics and Visualizations**
- Open the "Dashboard" in the navigation menu.
- Explore metrics like:
   1) Total deliveries
   2) Average delivery times
   3) Top delivery zones
   4) Resource utilization
- Use visualizations like maps, bar charts, and trend lines to understand the data and make informed decisions.
  
# Accessing the Application
- API Endpoint: http://localhost:5000
- Dashboard: http://localhost:8501 
  
# Tips for Best Use
- Regularly update order and route information to get accurate predictions and optimizations.
- Use the dashboard metrics to identify areas for improvement, such as frequently delayed routes.
- Optimize routes for large batches of orders to maximize efficiency.
