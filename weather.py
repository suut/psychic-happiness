#!/usr/bin/python3.4
# -*- coding: utf-8 -*-


#TODO: support weather codes: http://www.hamweather.com/support/documentation/aeris/codedweather/

class NotFoundException(Exception):
    pass

import urllib.parse, requests, json

weather_api = {'id': '',
               'secret': ''}

base_url = 'http://api.aerisapi.com/forecasts/'

mph2kmh = lambda x: str(round(1.609344*x, 2))


def deg2card(deg):
    if 0 <= deg <= 22.5 or 337.5 <= deg <= 359:
        return 'Nord'
    if 22.5 <= deg <= 67.5:
        return 'Nord-Est'
    if 67.5 <= deg <= 112.5:
        return 'Est'
    if 112.5 <= deg <= 157.5:
        return 'Sud-Est'
    if 157.5 <= deg <= 202.5:
        return 'Sud'
    if 202.5 <= deg <= 247.5:
        return 'Sud-Ouest'
    if 247.5 <= deg <= 292.5:
        return 'Ouest'
    if 292.5 <= deg <= 337.5:
        return 'Nord-Ouest'


class WeatherResponse:
    def __init__(self, data):
        self.json = json.loads(data)
        if not self.json['success']:
            raise NotFoundException('location not found')
        self.weatherdata = self.json['response'][0]['periods'][0]

    @property
    def windspeed(self):
        return mph2kmh(self.weatherdata['windSpeedMPH'])+' km/h'

    @property
    def abstract(self):
        return self.weatherdata['weatherPrimary']

    @property
    def averagetemp(self):
        return str(self.weatherdata['avgTempC'])+'°C'

    @property
    def feelsliketemp(self):
        return str(self.weatherdata['feelslikeC'])+'°C'

    @property
    def precipmm(self):
        return str(self.weatherdata['precipMM'])+' mm'

    @property
    def winddir(self):
        return deg2card(self.weatherdata['windDirDEG'])

    @property
    def humidity(self):
        return str(self.weatherdata['humidity'])+'%'

    @property
    def maxtemp(self):
        return str(self.weatherdata['maxTempC'])+'°C'

    @property
    def mintemp(self):
        return str(self.weatherdata['minTempC'])+'°C'


def weatherget(location):
    url = base_url+location+'?'
    params = {'from': 'today',
              'to': 'today',
              'client_id': weather_api['id'],
              'client_secret': weather_api['secret']}
    return WeatherResponse(requests.get(url+urllib.parse.urlencode(params)).content.decode())
