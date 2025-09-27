"""
reporter.py

Command-line application that uses live data to report data for a city using OpenWeatherMap API.
Displays a summary in the terminal and exports results to FILENAME.
"""

# Standard library
import os  # Retrieve API key from system environment
import csv  # Read and write CSV files

# Third-party libraries
from dotenv import load_dotenv  # Access API key from .env file
import requests  # HTTP requests to OpenWeatherMap API

load_dotenv()  # Load API key from .env
API_KEY = os.getenv('API_KEY')
FILENAME = 'city_data.csv'

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

    Sends a GET request to API, parses the response JSON, and extracts key data:
    - city name
    - country code
    - temperature
    - humidity
    - weather description

    Prevents crashes on invalid city names and malformed API JSON responses.

    Args:
        city (str): The city name to retrieve data for.

    Returns:    
        dict: Dictionary with keys 'city', 'country', 'temperature', 'humidity',
            and 'description' if successful.
        None: Returned if JSON parsing fails or the city is invalid.
    """
    url = 'http://api.openweathermap.org/data/2.5/weather'
    parameters = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # Temperature in Celsius
    }

    try:
        response = requests.get(url, params=parameters, timeout=5)
        response.raise_for_status()  # Raises an HTTPError for 4xx or 5xx responses

        try:
            data = response.json()  # Parses JSON into Python dict
        except ValueError as e:
            print(f"Failed to parse JSON: {e}")
            return None

        # Pulls only key data from the API response
        key_city_data = {
            'city': data.get('name'),
            'country': data['sys']['country'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description']
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
    Raw description stored in CSV remains unmodified.

    Args:
        city_data (dict): Dictionary containing the city's key information.
    """
    if city_data:
        print(f"\n--- Weather Report ---")
        print(f"City: {city_data['city']}, {city_data['country']}")
        print(f"Temperature: {round(city_data['temperature'])}°C")
        print(f"Humidity: {city_data['humidity']}%")
        print(f"Description: {city_data['description'].capitalize()}")
    else:
        print("Failed to retrieve data. Check city name or API key.")


def write_to_csv(city_data, filename=FILENAME):
    """
    Writes extracted city data to a CSV file with column headers.

    Uses a context manager ('with' statement) for safe file handling.

    Args:
        city_data (dict): Dictionary containing the city's key information.
        filename (str, optional): Name of the output CSV file. Defaults to FILENAME.
    """
    if city_data:
        headers = ['City', 'Country', 'Temperature (C)', 'Humidity (%)', 'Description']

        try:
            with open(filename, mode='w') as file:
                writer = csv.writer(file)
                writer.writerow(headers)

                writer.writerow([
                    city_data['city'],
                    city_data['country'],
                    city_data['temperature'],  # Stores raw float
                    city_data['humidity'],
                    city_data['description']  # Stores raw description without capitalization
                ])

            print(f"\n--- CSV Export ---")
            print(f"Data for {city_data['city']} written to {filename} successfully.")
        except IOError as e:
            print(f"An error occurred while writing to CSV file: {e}")
    else:
        print("Data failed to write.")


def read_csv(filename=FILENAME):
    """
    Reads and reports data from a CSV file.

    Prints the current number of cities and their rounded temperatures.
    Keeps raw float values in the file.

    Args:
        filename (str, optional): Name or path of CSV file. Defaults to FILENAME.
    """
    try:
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            cities = list(reader)
        
        count = len(cities)
        print(f"\n--- CSV Summary ---")
        print(f"Total number of cities in {filename}: {count}")

        if count:
            print("Cities and their temperatures:")
            for city in cities:
                try:
                    temp = round(float(city['Temperature (C)']))
                except ValueError:
                    temp = 'N/A'  # invalid or missing temperature
                print(f"- {city['City']}: {temp}°C")
        else:
            print("No data found.")
    
    except FileNotFoundError:
        print(f"{filename} not found. Please check directory or file name.")
    except IOError as e:
        print(f"Error occurred while reading the CSV file: {e}")


if __name__ == "__main__":
    try:
        # Prompt user to enter city name
        city = get_city()

        # Pull data for the specified city
        city_data = get_city_data(city)
    
        # Print data to the terminal
        display_data(city_data)

        # Write and save data to FILENAME
        write_to_csv(city_data)

        # Read and report data from default FILENAME
        read_csv()
    except Exception as e:
        print(f"An unexpected error occurred during testing: {e}")
