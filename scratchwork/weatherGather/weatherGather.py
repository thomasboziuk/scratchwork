# -*- coding: utf-8 -*-

"""

Created on Thu Apr 16 15:09:02 2020



@author: Tom

"""


#to parse returned values from the API
import requests as req

#to allow us to connect to and write to our SQL database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


#set up DB connection
db_string = 'postgresql+psycopg2://$USER_NAME:$PASSWORD@$DOMAIN.$TLD:5432/$DB_NAME'
db = create_engine(db_string)
base = declarative_base()






#define openweathermap API key and location desired
apiKey = '$API_KEY'
lat = '$LAT'
long = '$LONG'
zipCode = '$ZIP'


#get current weather data from API
response = req.get('https://api.openweathermap.org/data/2.5/weather?zip='+zipCode+',us&appid='+apiKey)
#jsonify response
response.json()






#parse into useful variable names, was originally used for debugging. probably could be done faster
temp = response.json()['main']['temp']

temp_max = response.json()['main']['temp_max']

temp_min = response.json()['main']['temp_min']

humidity = response.json()['main']['humidity']

pressure = response.json()['main']['pressure']

feels_like = response.json()['main']['feels_like']

clouds_pct = response.json()['clouds']['all']

lat, long = response.json()['coord'].values()

sunrise = response.json()['sys']['sunrise']

sunset = response.json()['sys']['sunset']

visibility = response.json()['visibility']

weather_desc = response.json()['weather'][0]['description']

weather_gen = response.json()['weather'][0]['main']

wind_direction = response.json()['wind']['deg']

wind_speed = response.json()['wind']['speed']

time = response.json()['dt']

rain_1hr = response.json().get('rain',{'1h':0,'3h':0}).get('1h',0)
rain_3hr = response.json().get('rain',{'1h':0,'3h':0}).get('3h',0)






#insert the parsed values into our databse for storage and, later, retrieval
db.execute("""INSERT INTO weather_data (temperature, temp_max, temp_min, humidity, pressure, feels_like, clouds_pct,

                                          latitude, longitude, sunrise, sunset, visibility, weather_description,

                                          weather_general, wind_direction, wind_speed, time, rain_1hr) 

VALUES ({},{},{},{},{},{},{},{},{},{},{},{},'{}','{}',{},{},{},{})""".format(
temp, temp_max, temp_min, humidity, pressure, feels_like, clouds_pct, lat, long, sunrise, sunset, visibility, weather_desc,
weather_gen, wind_direction, wind_speed, time, rain_1hr))


