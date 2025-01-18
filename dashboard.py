import streamlit as st
import folium
from streamlit_folium import st_folium
from predictive_model import load_model, predict_delivery_time
from data_scraping import fetch_traffic_data, fetch_weather_data

st.set_page_config(page_title="Logistics Dashboard", layout="wide")
st.title("Logistics Dashboard")
st.write("Welcome to the Logistics Dashboard!")

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
    submit_button = st.form_submit_button(label="Submit Order")

    if submit_button:
        traffic = fetch_traffic_data(customer_location)
        weather = fetch_weather_data(customer_location)
        model = load_model()
        predicted_time = predict_delivery_time(model, {
            'distance': distance,
            'order_priority': priority,
            'traffic_level': traffic,
            'weather_conditions': weather
        })
        st.success(f"Predicted Delivery Time: {predicted_time:.2f} hours")
