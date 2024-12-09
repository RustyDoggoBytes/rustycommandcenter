# https://open-meteo.com/en/docs#latitude=40.4775&longitude=-104.9014&current=temperature_2m&hourly=&daily=&timezone=America%2FDenver&forecast_days=3
import requests

# https://www.reddit.com/r/filemaker/comments/14yrpb9/openmeteo_weather_api_integration_free_icons_free/
resp = requests.get(
    "https://api.open-meteo.com/v1/forecast?latitude=40.4775&longitude=-104.9014&current=temperature_2m&timezone=America%2FDenver&forecast_days=3"
)

print(resp.json())
