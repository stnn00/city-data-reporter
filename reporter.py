"""
reporter.py

Command-line application that uses live data to report data for a city using OpenWeatherMap API.
Displays a summary in the terminal and exports results to 'city_data.csv'.
"""

# Standard library
import os # Retrieve API key from system environment
import csv # Read and write CSV files

# Third-party libraries
from dotenv import load_dotenv # Access API key from .env file
import requests # HTTP requests to OpenWeatherMap API

load_dotenv() # Load API key from .env
API_KEY = os.getenv("API_KEY")

def get_city():
    """
    Prompt the user to enter a city name until non-empty string is provided.

    Returns:
        str: The city name entered by the user.
    """
    while True:
        city = input("Enter a city name: ").strip()
        if city:
            return city
        print("Please enter a valid city name.")


def get_city_data(city):
    """
    Retrieves key data for a city from the OpenWeatherMap API.

    Sends a GET request to API, parses the response JSON, and extracts key data.

    Args:
        city (str): The city name to retrieve data for.

    Returns:    
        dict: Dictionary with keys 'city', 'country', 'temperature', 'humidity',
            and 'description'.
        None: Returned if the API request fails or an error occurs.
    """
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

        # Pulls only key data from the API response
        key_city_data = {
            "city": data.get("name"),
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        }

        return key_city_data

    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred while retrieving data: {err}")
        return None


def display_data(city_data):
    """
    Prints a formatted summary for a city's key data to the terminal.

    Rounds temperature to the nearest whole number and capitalizes the
    weather description for improved readability.

    Args:
        city_data (dict): Dictionary containing the city's key information.
    """
    if city_data:
        print(f"\nCity: {city_data['city']}, {city_data['country']}")
        print(f"Temperature: {round(city_data['temperature'])}°C")
        print(f"Humidity: {city_data['humidity']}%")
        print(f"Description: {city_data['description'].capitalize()}")
    else:
        print("Failed to retrieve data. Check city name or API key.")


def write_to_csv(city_data, filename="city_data.csv"):
    """
    Writes extracted city data to a CSV file with column headers.

    Uses a context manager ('with' statement) for safe file handling.

    Args:
        city_data (dict): Dictionary containing the city's key information.
        filename (str, optional): Name of the output CSV file. Defaults to 'city_data.csv'.
    """
    if city_data:
        headers = ["City", "Country", "Temperature", "Humidity (%)", "Description"]

        try:
            with open(filename, mode="w") as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                
                writer.writerow([
                    city_data["city"],
                    city_data["country"],
                    round(city_data["temperature"]),
                    city_data["humidity"],
                    city_data["description"].capitalize()
                ])

            print(f"\nData for {city_data['city']} written to {filename} successfully.")
        except IOError as e:
            print(f"An error occured while writing to CSV file: {e}")
    else:
        print("Data failed to write.")


def read_csv(filename="city_data.csv"):
    """
    Reads and reports data from a CSV file.

    Prints the current number of cities and temperatures in a CSV file.

    Args:
        filename(str, optional): Name or path of CSV file. Defaults to 'city_data.csv'.
    """
    try:
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            cities = list(reader)
        
        count = len(cities)
        print(f"\nTotal number of cities in {filename}: {count}")

        if count:
            print("Cities and their temperatures:")
            for city in cities:
                print(f"- {city['City']}: {city['Temperature']}°C")
        else:
            print("No data found.")
    
    except FileNotFoundError:
        print(f"{filename} not found. Please check directory or file name.")


if __name__ == "__main__":
    # Prompt user to enter city name
    city = get_city()

    # Pull data for the specified city
    city_data = get_city_data(city)
    
    # Print data to the terminal
    display_data(city_data)

    # Write and save data to 'city_data.csv'
    write_to_csv(city_data)

    # Read and report data from 'city_data.csv'
    read_csv("city_data.csv")
