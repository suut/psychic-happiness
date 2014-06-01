#!/usr/bin/python3.2
# -*- coding: utf-8 -*-

import re, requests, bs4


def parse(text):
    #returns formatted title of the link, or None
    links = re.findall(r'(https?://\S+)', text)
    if len(links) >= 1:
        print('found link(s):', '; '.join(links))
        url = links[0]
        #let's verify if it's html
        if 'text/html' in requests.head(url).headers.get('content-type'):
            return bs4.BeautifulSoup(requests.get(url).content).title.string
