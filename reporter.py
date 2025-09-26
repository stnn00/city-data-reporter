"""
reporter.py

A command-line application that uses live data to report
information about a city using OpenWeatherMap API,
writes the data to a CSV file called city_data.csv
"""

# Standard library
import os # Retrieve API key from system environment

# Third-party libraries
from dotenv import load_dotenv # Access API key from .env file
import requests # HTTP requests to OpenWeatherMap API

# Load .env file and get API key
load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_city():
    """Prompt user to enter a city name until non-empty city name is provided."""
    while True:
        city = input("Enter a city name: ").strip()
        if city:
            return city
        print("Please enter a valid city name.")

def get_city_data(city):
    """Retrieve data for user prompted city using OpenWeatherMap API."""
    url = "http://api.openweathermap.org/data/2.5/weather"
    parameters = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=parameters, timeout=5)
        response.raise_for_status() # Raises an HTTPError for 4xx or 5xx responses
        data = response.json()
        return data
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")
        return None


if __name__ == "__main__":
    city = get_city()
    print(f"User entered: {city}")
    weather_data = get_city_data(city)
    if weather_data:
        print("City data retrieved successfully.")
        print(weather_data)
    else:
        print("Failed to retrieve data. Check city name or API key.")