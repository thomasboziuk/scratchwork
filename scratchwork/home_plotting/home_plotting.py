# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker





#define up SQL connection
db_string = 'postgresql+psycopg2://$USER_NAME:$PASSWORD@$DOMAIN.$TLD:5432/$DB_NAME'
db = create_engine(db_string)
base = declarative_base()

#setup flask and dash
server = Flask(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, server = server, external_stylesheets=external_stylesheets)

#This is where we build our webpage layout. Part of serving the layout includes gathering the data from the last week. If you had a lot of requests, you would probably want to cache it and only update the data you need to, when you receive a new request. You could also want to spawn more workers in the .ini file, possibly.
def serve_layout():
    #grab the data we collected using our microcontroller
    result_set = db.execute("SELECT * FROM esp32data WHERE time > current_timestamp - interval '7 day' ORDER BY time ASC")
    result_list = [i for i in result_set]
    temperature_list = [i[2] for i in result_list]
    time_list = [i[0] for i in result_list]
    humidity_list = [i[4] for i in result_list]
    
    #grab the data we collected using the openweathermap API
    weather_data = db.execute("SELECT temperature, humidity, time_inserted FROM weather_data WHERE time_inserted > current_timestamp - interval '7 day' ORDER BY time_inserted ASC")
    exterior_weather = [i for i in weather_data]
    exterior_temperature = [(float(i[0])-273.15)*9/5+32 for i in exterior_weather]
    exterior_humidity = [float(i[1]) for i in exterior_weather]
    exterior_time =[i[2] for i in exterior_weather]
    x = [i for i in range(len(result_list))]

    #what we return is html. Dash (dcc) helps us build javascript/plotly charts in this quickly and easily.
    return  html.Div(children=[
    html.H1(children='Hello Friends'),

    html.Div(children='''
        Building off a Dash example, we can plot our gathered data. These are values gathered at my desk.
They are compared to values of the exterior weather, gathered from a weather API service.
    '''),
    #where the actual plotting happens. the esp32 data is downsampled by a factor of 8 because it wasn't loading fast enough.
    dcc.Graph(
        id='gathered_data',
        figure={
            'data': [
                {'x': time_list[::8], 'y': temperature_list[::8], 'type': 'scatter', 'mode':'lines+markers','name': 'T'},
                {'x': time_list[::8], 'y': humidity_list[::8], 'type': 'scatter', 'mode':'lines+markers','name': u'H'},
		{'x': exterior_time, 'y': exterior_temperature, 'type': 'scatter', 'mode': 'lines','name':'T_exterior'},
		{'x': exterior_time, 'y': exterior_humidity, 'type': 'scatter', 'mode': 'lines','name':'H_exterior'}
            ],
            'layout': {
                'title': 'ESP32 data'
            }
        }
    )

])




app.layout = serve_layout



if __name__ == '__main__':
    app.run_server(host = '0.0.0.0',debug = True)
