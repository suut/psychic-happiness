# -*- coding: utf-8 -*-

import urllib.request, urllib.parse, json

credentials = {'cx':'', #PLEASE CHANGE THIS
               'key': ''} #and optionnally this

class SearchQuery:  
    def __init__(self, query, cred=credentials, quotaUser='', prettyPrint='false', safe='off', lang='fr', nb=1, index=1):
        self.params = {'prettyPrint': prettyPrint,
                       'quoteUser': quotaUser,
                       'cx': cred['cx'],
                       'key': cred['key'],
                       'safe': safe,
                       'lr': 'lang_'+lang,
                       'num': nb,
                       'start': index,
                       'q': query}
    @property
    def url(self):
        return 'https://www.googleapis.com/customsearch/v1?'+urllib.parse.urlencode(self.params)

class YoutubeQuery:
    def __init__(self, query, cred=credentials):
        self.params = {'part': 'snippet',
                       'maxResults': '1',
                       'q': query,
                       'type': 'video',
                       'key': cred['key']}

    @property
    def url(self):
        return 'https://www.googleapis.com/youtube/v3/search?'+urllib.parse.urlencode(self.params)

class SearchResponse:
    def __init__(self, data):
        self._json = json.loads(data.decode())
        self._item = self._json['items'][0]
    @property
    def total_results(self):
        return self._json['searchInformation']['formattedTotalResults']
    @property
    def search_time(self):
        return self._json['searchInformation']['formattedSearchTime']
    @property
    def title(self):
        return self._item['title']
    @property
    def link(self):
        return self._item['link']
    @property
    def display_url(self):
        return self._item['displayLink']
    @property
    def abstract(self):
        return self._item['snippet'].replace('\n', '').replace('\xA0', '')
    def display(self):
        return '{0} — {1}\n{2}\n{3}'.format(self.display_url, self.title, self.abstract, self.link)

class YoutubeResponse:
    def __init__(self, data):
        self._json = json.loads(data.decode())
        self._item = self._json['items'][0]
    @property
    def title(self):
        return self._item['snippet']['title']
    @property
    def id(self):
        return self._item['id']['videoId']
    @property
    def description(self):
        return self._item['snippet']['description']
    @property
    def channel(self):
        return self._item['snippet']['channelTitle']
    def display(self):
        return '{0} — {1}\n{2}\nhttp://youtu.be/{3}'.format(self.title, self.channel, self.description, self.id)

def ytquery(ytsearchquery):
    return YoutubeResponse(urllib.request.urlopen(ytsearchquery.url).read())

def query(searchquery):
    return SearchResponse(urllib.request.urlopen(searchquery.url).read())

def shortenUrl(urlprovided, cred=credentials):
    url = 'https://www.googleapis.com/urlshortener/v1/url?fields=id&key={0}'.format(cred['key'])
    data = json.dumps({'longUrl':urlprovided}).encode('iso-8859-1')
    req = urllib.request.Request(url,data)
    req.add_header('Content-type', 'application/json')
    data = urllib.request.urlopen(req).read().decode('iso-8859-1')
    js = json.loads(data)
    return js['id']

def expandUrl(urlprovided, cred=credentials):
    url = 'https://www.googleapis.com/urlshortener/v1/url?'+urllib.parse.urlencode({'key': cred['key'],
                                                                                    'shortUrl': urlprovided})
    try:
        data = urllib.request.urlopen(url).read().decode('iso-8859-1')
    except urllib.error.HTTPError:
        return 'Bad URL.'
    js = json.loads(data)
    return js['longUrl']
