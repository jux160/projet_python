import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import csv
def meteo(ville):
    """fonction renvoyant la temperature de la ville passer en parametre 

    Args:
        ville (str): ville dont on veux la temperature 

    Returns:
        : temperature de la ville demander 
    """
    city = []

    with open("cities.csv", mode="r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["city_code"] == ville:
                city.append(row)

    # setup de l'api meteo et gestion des erreur de conneion a l'api 
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://api.open-meteo.com/v1/meteofrance"
    params = {
        "latitude": city[0]["latitude"],
        "longitude": city[0]["longitude"],
        "current": "temperature_2m"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    #print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    #print(f"Elevation {response.Elevation()} m asl")
    #print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    #print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()

    print(f"Current time {current.Time()}")
    print(f"Current temperature_2m {current_temperature_2m}")
    return current_temperature_2m
