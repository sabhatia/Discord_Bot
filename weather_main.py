import requests
import os
from dotenv import load_dotenv
from typing import Final
from datetime import datetime
from pprint import pprint
import json

class Weather:
    
    BASE_DOMAIN: Final[str] = "api.meteomatics.com"
    PARAM_TEMP: Final[str] = "t_2m:C"
    PARAM_WIND_SPEED: Final[str] = "wind_speed_10m:ms"
    PARAM_WIND_DIREC: Final[str] = "wind_dir_10m:d"
    PARAM_UV: Final[str] = "uv:idx"
    RETURN_TYPE: Final[str] = "json"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.url = 'https://' + self.username + ':' + self.password + '@' + self.BASE_DOMAIN

    def build_request(self, weather_time, weather_zip_code):
        # Get the ISO 8601 time for current time

        return(self.url + '/' + weather_time \
        + '/' + self.PARAM_TEMP + ',' + self.PARAM_UV + ',' + self.PARAM_WIND_DIREC \
        + ',' + self.PARAM_WIND_SPEED \
        + '/' + weather_zip_code \
        + '/' + self.RETURN_TYPE)
    
    def get_weather_data(self, weather_request: str):
        try:
            response = requests.get(weather_request)
        except requests.exceptions.RequestException as e:
            print(f'Requests Error: {e}')

        return response
    
    def parse_weather_rsp(self, weather_rsp: requests.Response):
        rsp_body = json.loads(weather_rsp.text)
        temp = rsp_body['data'][0]['coordinates'][0]['dates'][0]['value']
        uv_indx = rsp_body['data'][1]['coordinates'][0]['dates'][0]['value']
        wind_dir = rsp_body['data'][2]['coordinates'][0]['dates'][0]['value']
        wind_speed = rsp_body['data'][3]['coordinates'][0]['dates'][0]['value']

        return temp, uv_indx, wind_dir, wind_speed

def weather_main():
    # Get env data
    load_dotenv()
    WEATHER_USER = os.getenv('METOMATICS_USERNAME')
    WEATHER_PASS = os.getenv('METOMATICS_PASSWORD')

    # Build a request
    local_weather: Weather = Weather(WEATHER_USER, WEATHER_PASS)
    sjc_iso_time: str = datetime.now().isoformat()
    # Get the current datetime
    sjc_iso_time = datetime.now().strftime("%Y-%m-%dT%H:%MZ")
    sjc_location: str = '37.2752,121.6853'

    print(f'Date: {sjc_iso_time}')
    weather_req: str = local_weather.build_request(sjc_iso_time, sjc_location)
    print(f'Request: {weather_req}')

    # Send the request and get a response
    rsp = local_weather.get_weather_data(weather_req)
    print(f'Response: {rsp.text}')
    rsp_body = json.loads(rsp.text)

    # Extract the data
    temp = rsp_body['data'][0]['coordinates'][0]['dates'][0]['value']
    uv_indx = rsp_body['data'][1]['coordinates'][0]['dates'][0]['value']
    wind_dir = rsp_body['data'][2]['coordinates'][0]['dates'][0]['value']
    wind_speed = rsp_body['data'][3]['coordinates'][0]['dates'][0]['value']

    print(f'Today\'s Weather\nTemp: {temp}\xb0 C\nUV-Index (0-12): {uv_indx}\nWind Speed: {wind_speed} m/s\nWind Direction: {wind_dir}\xb0')
    
    #Re-Extra the data
    temp1, uv_indx1, wind_dir1, wind_speed1 = local_weather.parse_weather_rsp(rsp)
    print(f'Today\'s Weather\nTemp: {temp1}\xb0 C\nUV-Index (0-12): {uv_indx1}\nWind Speed: {wind_speed1} m/s\nWind Direction: {wind_dir1}\xb0')

if __name__ == '__main__':
    weather_main()

