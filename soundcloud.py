#!/usr/bin/python3.2
# -*- coding: utf-8 -*-

import urllib.parse, requests, bs4

api_key = 'd4e48cd67bf3ec300e0d9752a450a3f4'

def soundcloud_search(query):
    api_url = 'http://api.soundcloud.com/tracks?'
    params = {'client_id': api_key,
              'q': query,
              'limit': '1'}
    url = api_url+urllib.parse.urlencode(params)
    soup = bs4.BeautifulSoup(requests.get(url).content)
    if soup.findChild('track') is None:
        return None
    soup = soup.tracks.track
    return {'title': soup.title.text,
            'url': soup.findChild('permalink-url', recursive=False).text,
            'username': soup.user.username.text,
            'genre': soup.genre.text,
            'likes': soup.findChild('favoritings-count', recursive=False).text,
            'timesplayed': soup.findChild('playback-count', recursive=False).text,
            'tracktype': soup.findChild('track-type', recursive=False).text,
            'description': soup.description.text}
