Weather Display Setup Guide
===========================

This script fetches real-time weather data for the specified latitude and longitude using the Open-Meteo API. It generates a two-frame animated GIF:

*   **Frame 1:** Displays the current weather condition icon (e.g., sunny, cloudy, rainy) based on the weather code.
*   **Frame 2:** Displays the current temperature in Celsius, rendered with a dynamic colour that corresponds to the temperature range (e.g., cooler tones for low temperatures, warmer tones for high temperatures).

The generated GIF is automatically sent to the connected dot-matrix display via the `python3-idotmatrix-client` [library](https://github.com/derkalle4/python3-idotmatrix-client). By default, the script updates the weather information every 30 minutes, but this interval can be customised in the configuration file (`config.ini`).

Step 1: Ensure Prerequisites
----------------------------

Make sure the `python3-idotmatrix-client` is installed or accessible in your Python environment. If it is not, navigate to the `python3-idotmatrix-client` directory and install it using:

    pip install .

Step 2: Install Dependencies
----------------------------

Navigate to the `idotmatrix-weather` directory in your console and run:

    pip install requests pillow

Step 3: Set Up `config.ini`
---------------------------

Edit the `config.ini` file to update the following parameters as needed:

*   `latitude`: Your location's latitude
*   `longitude`: Your location's longitude
*   `timezone`: Your location's timezone using [TZ format](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
*   `device_address`: Address of your display device gathered from the python3-idotmatrix-client with the `--scan` command
*   `frame_duration`: Duration of each frame in milliseconds (eg.g, 1000 = 1 second)
*   `update_interval`: Update interval in seconds (e.g., 1800 = 30 minutes). Please respect the Open-Meteo API and don't set this to update too often.

    [settings]
    latitude = YOUR_LATTITUDE
    longitude = YOUR_LONGITUDE
    timezone = YOUR_TIMEZONE
    device_address = YOUR_DEVICE_ADDRESS
    frame_duration = 3000
    update_interval = 1800
    
    

Step 4: Run the Script
----------------------

Execute the script to fetch weather data, generate a GIF, and send it to the display:

    python weather_display.py

Step 5: Verify and Debug
------------------------

Check the console for debug messages and `debug` directory for generated GIFs or rendered frames in case of issues.

Notes
-----

*   idotmatrix-weather script by:
    *   [@artywah.bsky.social](https://bsky.app/profile/artywah.bsky.social)
    *   With a lot of help from ChatGPT
*   Weather data provided by:
    *   [Open-Meteo](https://open-meteo.com/en/terms)
    *   License: Free for non-commercial use
*   Original weather icons:

*   Source: [Iconset: Weather Color](https://www.iconfinder.com/iconsets/weather-color-2)
*   Author: Sihan Liu
*   License: Free for commercial use
