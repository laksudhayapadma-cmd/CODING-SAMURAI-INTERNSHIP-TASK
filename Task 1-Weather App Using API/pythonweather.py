import requests          # For making HTTP calls to the API
import json              # For reading the API's JSON response
import sys               # For clean program exit on errors
from config import API_KEY, BASE_URL   # Import our stored settings


def kelvin_to_celsius(kelvin_temp):
    """
    Converts temperature from Kelvin (API default) to Celsius.
    Formula: subtract 273.15 from Kelvin value.
    """
    return round(kelvin_temp - 273.15, 2)


def kelvin_to_fahrenheit(kelvin_temp):
    """
    Converts Kelvin to Fahrenheit for users who prefer it.
    Formula: (K - 273.15) × 9/5 + 32
    """
    celsius = kelvin_to_celsius(kelvin_temp)
    return round((celsius * 9 / 5) + 32, 2)


def fetch_weather_data(city_name):
    """
    Sends a GET request to OpenWeatherMap API.
    Returns the full JSON response as a Python dictionary.
    Handles connection errors and invalid city names.
    """
    query_params = {
        "q": city_name,       # City name typed by user
        "appid": API_KEY,     # Our API authentication key
    }

    try:
        response = requests.get(BASE_URL, params=query_params, timeout=10)

        # HTTP 200 means success; anything else triggers an error
        if response.status_code == 200:
            return response.json()   # Convert JSON string → Python dict

        elif response.status_code == 401:
            print("\n❌ Error: Invalid API key. Check your config.py file.")
            sys.exit(1)

        elif response.status_code == 404:
            print(f"\n❌ Error: City '{city_name}' not found. Check spelling.")
            return None

        else:
            print(f"\n❌ Unexpected error. Status code: {response.status_code}")
            return None

    except requests.exceptions.ConnectionError:
        print("\n❌ No internet connection. Please check your network.")
        sys.exit(1)

    except requests.exceptions.Timeout:
        print("\n❌ Request timed out. Try again in a moment.")
        sys.exit(1)


def extract_and_display(data, city_name):
    """
    Pulls specific fields from the API response dictionary.
    Formats and prints the weather report neatly to the terminal.
    """

    temperature_k  = data["main"]["temp"]           # Temp in Kelvin
    feels_like_k   = data["main"]["feels_like"]     # Feels-like in Kelvin
    humidity       = data["main"]["humidity"]        # Percentage
    wind_speed     = data["wind"]["speed"]           # Meters per second
    description    = data["weather"][0]["description"]  # e.g. "clear sky"
    country_code   = data["sys"]["country"]          # e.g. "IN", "US"
    visibility     = data.get("visibility", "N/A")   # Meters (not always present)

    temp_c  = kelvin_to_celsius(temperature_k)
    temp_f  = kelvin_to_fahrenheit(temperature_k)
    feels_c = kelvin_to_celsius(feels_like_k)

    wind_kmh = round(wind_speed * 3.6, 1)

    visibility_km = f"{round(visibility / 1000, 1)} km" if isinstance(visibility, int) else "N/A"

    print("\n" + "=" * 45)
    print(f"  🌍  WEATHER REPORT — {city_name.upper()}, {country_code}")
    print("=" * 45)
    print(f"  🌤️  Condition     : {description.title()}")
    print(f"  🌡️  Temperature   : {temp_c}°C  /  {temp_f}°F")
    print(f"  🤔  Feels Like    : {feels_c}°C")
    print(f"  💧  Humidity      : {humidity}%")
    print(f"  💨  Wind Speed    : {wind_kmh} km/h")
    print(f"  👁️  Visibility    : {visibility_km}")
    print("=" * 45 + "\n")


def run_weather_app():
    """
    Main controller function.
    Handles the user input loop and ties everything together.
    """

    print("\n🌦️  Welcome to Python Weather App")
    print("   Powered by OpenWeatherMap API\n")

    while True:
        city_input = input("Enter city name (or 'quit' to exit): ").strip()

        if city_input.lower() in ["quit", "exit", "q"]:
            print("\n👋 Thanks for using Weather App. Goodbye!\n")
            break

        if not city_input:
            print("⚠️  Please enter a city name.\n")
            continue

        weather_data = fetch_weather_data(city_input)

        if weather_data:
            extract_and_display(weather_data, city_input)


if __name__ == "__main__":
    run_weather_app()