import requests

# API Keys
TRAFFIC_API_KEY = 'your_traffic_api_key'
WEATHER_API_KEY = 'your_weather_api_key'

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
