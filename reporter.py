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

# Load .env file and get API key
load_dotenv()
API_KEY = os.getenv("API_KEY")


def input_city():
    """Prompt user to enter a city name until non-empty city name is provided."""
    while True:
        city = input("Enter a City name: ").strip() # Remove leading/trailing whitespaces
        if city:
            return city
        print("City name cannot be empty. Please enter a non-empty city name.")


if __name__ == "__main__":
    city = input_city()
    print(f"User entered: {city}")