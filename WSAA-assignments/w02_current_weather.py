# week 2 assignment 
# Assignment: current weather
# Author: Norbert Antal

import requests #module to manage HTTP requests
import json #module to manage JSON data

#store coordinates for location based API request
lon=-6.460040
lat=52.339230
#dynamic URL based on above coordinates for the API request
url=f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
#get data from API and convert to python dictionary
response = requests.get(url)#Sends an HTTP GET request to the specified URL and stores the response.
data = response.json()#parse data from JSON format into a python dictionary
#access data
current = data["current"] #"current" is the key or head or name to select the measurement values section of the dictionary
units = data["current_units"] #"current_units" points to the measurement units section of the dictionary
#store data for output - dictionary labels taken from the output from the url viewed in browser
#get values 
temperature = current["temperature_2m"]
wind = current["wind_speed_10m"]
#get measurement units
u_temperature = units["temperature_2m"] 
u_wind = units["wind_speed_10m"]
#outputs current temperature and wind values with their respective units to consol
print(url)
print(f"\nCurrent temperature at 2m: {temperature}{u_temperature}, \nCurrent wind speed at 10m: {wind}{u_wind}\n")