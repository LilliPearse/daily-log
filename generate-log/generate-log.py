import requests
from datetime import datetime
import os

LOG_DIR = "logs"

WEATHER_ASCII = {
    "sunny": """\
   \\   /
    .-.
 ― (   ) ―
    `-’
   /   \\
Sunny""",
    "cloudy": """\
     .--.
  .-(    ).
 (___.__)__)
Cloudy""",
    "rainy": """\
     .-.
    (   ).
   (___(__)
   ‘ ‘ ‘ ‘
   ‘ ‘ ‘ ‘
Rainy""",
    "snowy": """\
     .-.
    (   ).
   (___(__)
   * * * *
   * * * *
Snowy"""
}

def get_coordinates(location):
    url = f"https://nominatim.openstreetmap.org/search"
    params = {"q": location, "format": "json", "limit": 1}
    headers = {"User-Agent": "github-weather-logger"}
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    results = response.json()
    if not results:
        raise Exception(f"No coordinates found for location '{location}'.")
    lat = float(results[0]["lat"])
    lon = float(results[0]["lon"])
    print(f"Found coordinates for {location}: {lat:.2f}, {lon:.2f}")
    return lat, lon

def get_weather_description(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weathercode"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    weather_code = data["current"]["weathercode"]

    if weather_code in [0, 1]:
        return WEATHER_ASCII["sunny"]
    elif weather_code in [2, 3]:
        return WEATHER_ASCII["cloudy"]
    elif 50 <= weather_code <= 67 or 80 <= weather_code <= 82:
        return WEATHER_ASCII["rainy"]
    elif 71 <= weather_code <= 77 or 85 <= weather_code <= 86:
        return WEATHER_ASCII["snowy"]
    else:
        return "Weather unavailable"

def get_quote_of_the_day():
    quote_of_the_day = input("Quote of the day: ")
    return quote_of_the_day

def create_log_file(date_str, location, weather_ascii, quote_of_the_day ):
    filename = os.path.join(LOG_DIR, f"{date_str}.txt")
    os.makedirs(LOG_DIR, exist_ok=True)

    with open(filename, "w") as file:
        file.write(f"Date: {date_str}\n")
        file.write(f"Location: {location}\n")
        file.write("Weather:\n")
        file.write(f"{weather_ascii}\n\n")
        file.write("Quote of the day:\n")
        file.write(f"{quote_of_the_day}\n")

    print(f"Log created: {filename}")

if __name__ == "__main__":
    import sys

    date_str = datetime.today().strftime("%Y-%m-%d")
    if len(sys.argv) > 1:
        date_str = sys.argv[1]

    location = input("Enter a general location (e.g., 'London', 'Yorkshire'): ")
    latitude, longitude = get_coordinates(location)

    weather_ascii = get_weather_description(latitude, longitude)

    quote_of_the_day = get_quote_of_the_day()

    create_log_file(date_str, location, weather_ascii, quote_of_the_day)
