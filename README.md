# city-data-reporter

A Python command-line tool that fetches real-time weather data for any city, displays key information in clear terminal output, exports raw data to a CSV file, and securely loads the OpenWeatherMap API key from a `.env` file.

All functionality is contained in a single Python Script: `reporter.py`

---

## Features

- Access real-time weather data for any city.
- Display key information in a clear, formatted output: city, country, temperature, humidity, and weather description in a readable format.
- Export collected raw weather data to a `.csv` file (default file is `city_data.csv`; currently, it overwrites the file each time, it does **not** append).
- Temperatures are rounded for terminal readability, but precise values are preserved in the `.csv` file.
- CSV file includes column headers for spreadsheet integration.
- Automatically loads API key from a `.env` file for security.
- Simple, user-friendly terminal interface.

---

## Demonstration

Video on Youtube to demonstrate and explain code `reporter.py`:

- *INSERT_LINK_HERE*

---

## Installation

1. **Install Python 3**.

    Ensure [Python 3](https://www.python.org/downloads/) is installed on your system.
    
2. **Install required third-party packages**:

    ``` bash
    pip install requests python-dotenv
    ```

3. **Obtain an [OpenWeatherMap](https://openweathermap.org/) API key**:

    1. Register for a free account on [OpenWeatherMap](https://home.openweathermap.org/users/sign_up).
    2. Navigate to "My API keys" OR click on your profile and select "API keys".
    3. Create a `.env` file in the project directory with the following content:

        ```env
        API_KEY=your_api_key_here
        ```

        ***Do NOT share your API key publicly.***

4. **Clone the repository**.
   ```bash
   git clone https://github.com/stnn00/city-data-reporter.git
   cd city-data-reporter
   ```

   ---

## Instructions
1. **Run the program**:
    ```bash
    python reporter.py
    ```

2. **Enter a city name when prompted.**

    Example of Prompt:
    ```text
    Enter a city name:
    ```

3. **The program will**:
    - Display the city's key data to the terminal.
    - Export the raw data to `city_data.csv`. (note: this will overwrite any existing file with the same name).

**Example Terminal Output**:
```text
Enter a city name: Albertville

--- Weather Report ---
City: Albertville, US
Temperature: 21°C
Humidity: 85%
Description: Clear sky

--- CSV Export ---
Data for Albertville written to city_data.csv successfully.

--- CSV Summary ---
Total number of cities in city_data.csv: 1
Cities and their temperatures:
- Albertville: 21°C
```

---

## Notes

- Ensure your `.env` file is in the same directory as `reporter.py`.
- The program exports data to `city_data.csv` by default. **This file will be overwritten each time the script runs; it does not append.**