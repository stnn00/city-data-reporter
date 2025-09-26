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
        "units": "metric" # Temperature in Celsius
    }

    try:
        response = requests.get(url, params=parameters, timeout=5)
        response.raise_for_status() # Raises an HTTPError for 4xx or 5xx responses
        data = response.json() # Uses JSON library to parse the response from API into dictionary

        key_city_data = {
            "city": data.get("name"),
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        }

        return key_city_data

    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")
        return None
    
def display_data(city_data):
    """
    Prints a formatted summary for the key data of the user-specified city.

    Temperature is rounded to the nearest whole number for readability.
    The weather description is capitalized for clarity.
    """
    if city_data:
        print(f"\nCity Name: {city_data['city']}")
        print(f"Country: {city_data['country']}")
        print(f"Temperature: {round(city_data['temperature'])}°C")
        print(f"Humidity: {city_data['humidity']}%")
        print(f"Weather Conditions: {city_data['description'].capitalize()}")
    else:
        print("Failed to retrieve data. Check city name or API key.")


if __name__ == "__main__":
    # Prompt user to enter a city, retrieves and prints key data.
    city = get_city()
    city_data = get_city_data(city)
    display_data(city_data)
    