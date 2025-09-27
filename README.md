# city-data-reporter

A Python command-line tool that fetches real-time weather data for any city, displays key information in clear terminal output, exports raw data to a CSV file, and securely loads the OpenWeatherMap API key from a `.env` file.

All functionality is contained in a single Python Script: `reporter.py`

## Features

- Access real-time weather data for any city.
- Display key information in a clear, formatted output: city, country, temperature, humidity, and weather description in a readable format.
- Temperatures are rounded for terminal readability, but precise values are preserved in the CSV.
- Export collected raw weather data to a CSV file.
- CSV file includes column headers for spreadsheet integration.
- Automatically loads API key from a `.env` file for security.
- Simple, user-friendly terminal interface