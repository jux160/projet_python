import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import csv

ville = input("choisisez le nom de votre ville ")
ville = ville.lower()

city = []

with open("cities.csv", mode="r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["city_code"] == ville:
            city.append(row)
print(city)
print(city[0]["latitude"])
print(city[0]["longitude"])
# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/meteofrance"
params = {
	"latitude": city[0]["latitude"],
	"longitude": city[0]["longitude"],
	"current": "temperature_2m"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Current values. The order of variables needs to be the same as requested.
current = response.Current()
current_temperature_2m = current.Variables(0).Value()

print(f"Current time {current.Time()}")
print(f"Current temperature_2m {current_temperature_2m}")

