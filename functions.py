#!/usr/bin/python3.2
# -*- coding: utf-8 -*-

from functions_core import Function, match
import functions_core
from core import server_config, version, stop
from random import sample
import format
import random
import datetime
import google
import soundcloud
import configparser
import weather
import importlib, admin, reload
import codecs ## For ROT13

functions_core.register = []
importlib.reload(admin)
importlib.reload(reload)


@Function('ping')
def ping(args, source, target):
    """pong!"""
    yield 'pong'

with open('strings/eloges.txt') as file:
    sarah_adjs = file.read().split('\n')

with open('strings/adjs.txt') as file:
    adjs = file.read().split('\n')

hatsu_adjs = ('execrable',
              'laide',
              'grosse',
              'abominable',
              'détestable',
              'épouvantable',
              'insalubre',
              'saccagée',
              'ravagée')


@Function('sarah')
def sarah(args, source, target):
    """vous dira qui est-ce... :)"""
    seed = int(''.join(args)) % len(sarah_adjs) if args is not None and ''.join(args).isdigit() else random.randint(0, len(sarah_adjs))
    yield 'la plus {0}'.format(sarah_adjs[seed])


@Function('hatsu', requestchans=True)
def hatsu(args, source, target, channels):
    """vous dira qui est-ce... :)"""
    if target[0] == '#' and 'hatsu' not in channels[target].userdict.keys():
        seed = int(''.join(args)) % len(hatsu_adjs) if args is not None and ''.join(args).isdigit() else random.randint(0, len(hatsu_adjs))
        yield 'la plus {0}'.format(hatsu_adjs[seed])
    else:
        seed = int(''.join(args)) % len(sarah_adjs) if args is not None and ''.join(args).isdigit() else random.randint(0, len(sarah_adjs))
        yield 'la plus {0}'.format(sarah_adjs[seed])


@Function('eyecancer')
def eyecancer(args, source, target):
    """just try it :)"""
    yield '13,10UNTZ2,3UNTZ2,7UNTZ2,7UNTZ6,13UNTZ12,5UNTZ4,10UNTZ11,6UNTZ9,13UNTZ4,13UNTZ3,11UNTZ3,' \
          '7UNTZ7,9UNTZ6,10UNTZ9,2UNTZ10,9UNTZ10,7UNTZ4,11UNTZ3,13UNTZ12,11UNTZ9,6UNTZ2,11UNTZ13,7UNTZ3,' \
          '9UNTZ13,10UNTZ2,10UNTZ8,2UNTZ10,5UNTZ9,10UNTZ9,4UNTZ6,4UNTZ6,9UNTZ7,8UNTZ8,13UNTZ5,11UNTZ10,' \
          '5UNTZ8,10UNTZ5,10UNTZ2,7UNTZ12,8UNTZ2,8UNTZ9,12UNTZ4,10UNTZ6,3UNTZ2,6UNTZ11,6UNTZ5,13UNTZ8,' \
          '3UNTZ11,4UNTZ2,11UNTZ6,7UNTZ'


@Function(['g', 'google'])
def search(args, source, target):
    """performs a search via Google"""
    if args is not None:
        q = google.SearchQuery(' '.join(args))
        try:
            r = google.query(q)
        except IndexError:
            yield 'no results'
            stop()
        yield '{color.bold}{}{color.reset} — {}\n{}\n' \
              '{color.bold}{color.underlined}{}{color.reset}'.format(r.title,
                                                                     r.display_url,
                                                                     r.abstract,
                                                                     r.link)
        stop()
    yield 'no query specified'


@Function(['yt', 'youtube'])
def youtube(args, source, target):
    """performs a search on YouTube"""
    if args is not None:
        q = google.YoutubeQuery(' '.join(args))
        try:
            r = google.ytquery(q)
        except IndexError:
            yield 'no results'
            stop()
        yield '{color.bold}{}{color.reset} — {}\n{}\n{color.bold}{color.underlined}http://youtu.be/{}{color.reset}'.format(r.title,
                                                                                                                           r.channel,
                                                                                                                           r.description,
                                                                                                                           r.id)
        stop()
    yield 'no query specified'


with open('strings/pornos.txt') as file:
    pornos = file.read().split('\n')

@Function('film')
def film(args, source, target):
    """un nom de "film" au hasard"""
    yield sample(pornos, 1)[0]


@Function('help')
def help(args, source, target):
    """provides help on commands"""
    if args is None:  # showing all functions
        list_of_cmds = []
        for f in functions_core.register:
            if isinstance(f.cmdname, list):
                list_of_cmds.append(' = '.join(f.cmdname))
            else:
                if 'is_action' not in dir(f) and f.authlvl == 'none':
                    list_of_cmds.append(f.cmdname)
        yield '{color.bold}commands are{color.reset}: {0}'.format(', '.join(list_of_cmds))
        yield 'to know more about a particular command type {0}help cmdname'.format(server_config['commands']['cmdprefix'][0])
        stop()
    elif len(args) != 1:
        yield 'syntax is cmdname'
        stop()
    else:
        for i in functions_core.register:
            if match(i, args[0].lower()):
                if i.doc is None:
                    yield 'command has no documentation'
                else:
                    yield '{color.bold}{}{color.reset}: {}'.format(args[0].lower(), i.doc)
                stop()
        yield 'unknown command "{0}"'.format(args[0].lower())


@Function('quisuisje')
def quisuisje(args, source, target):
    """détermine avec exactitude qui vous êtes, ou plutôt ce que vous êtes"""
    yield 'vous êtes plutôt...{0}'.format(adjs[hash(source.nick )%len(adjs)])


@Function('drugs')
def drugs(args, source, target):
    """provides a list of RC shops"""
    if target == '#psychonautfr':
        yield 'what the hell do you think you\'re doing??'
    else:
        yield 'http://rcshops.pastebay.net/1279926'


@Function('error')
def error(args, source, target):
    """to test handling of exceptions"""
    raise RuntimeError('FATAL ERROR')


@Function('source')
def source(args, source, target):
    """prints the URL of the source code (on github)"""
    yield '{color.bold}source code{color.reset}: https://github.com/suut/psychic-happiness/tree/v2/'


@Function('version')
def version_(args, source, target):
    """prints the actual bot version"""
    yield '{color.bold.red}' + version + '{color.reset}'
 n

with open('strings/drugs.txt') as file:
    list_drugs = file.read().split('\n')

@Function('dotd')
def dotd(args, source, target):
    """drug of the day :)"""
    seed = int('{0}{1}'.format(datetime.datetime.today().month, datetime.datetime.today().day))
    yield '{color.bold}drug of the day{color.reset}: ' + list_drugs[seed%len(list_drugs)]


@Function(['sc', 'soundcloud'])
def scsearch(args, source, target):
    """performs a search on soundcloud"""
    if args is not None:
        r = soundcloud.soundcloud_search(' '.join(args))
        if r is None:
            yield 'no results'
            stop()
        yield '{color.bold}{}{color.reset} — {}\n{}\n{color.underlined}{color.bold}{}{color.reset}'.format(r['title'],
                                                                                                           r['username'],
                                                                                                           r['description'].replace('\n', '').replace('\r', '')[:400],
                                                                                                           r['url'])
        stop()
    yield 'no query specified'


class Action:
    def __init__(self, name, one, many):
        self.name = name
        self._one = one
        self._many = many
        self.ppl = []

    def one_f(self, name):
        return self._one.format(name=name)

    def many_f(self, names):
        return self._many.format(names=type(self).sep(names))

    def f(self, args, source, target):
        """it's an action"""
        if args is not None and ''.join(args).strip() == '-clear':
            self.ppl = []
            yield 'nobody {0} anymore? :('.format(self.name)
            stop()
        if len(self.ppl) == 0:
            self.ppl.append(source.nick)
            yield self.one_f(source.nick)
            stop()
        else:
            if source.nick not in self.ppl:
                self.ppl.append(source.nick)
            if len(self.ppl) == 1:
                #just display the list
                yield self.one_f(self.ppl[0])
            else:
                yield self.many_f(self.ppl)

    @staticmethod
    def sep(names):
        seps = []
        n = ''
        for i in range(len(names)-2):
            seps.append(', ')
        seps.append(' and ')
        for i, j in zip(names, seps):
            n += i+j
        n += names[-1]
        return n

actionslist = []

actionsparser = configparser.ConfigParser()
actionsparser.read('strings/actions.ini')
actions = dict(actionsparser['actions'])

for key, val in zip(actions.keys(), actions.values()):
    name = key
    one, many = val.split(';')
    actionslist.append(Action(name, one, many))

for act in actionslist:
    f = Function(act.name)(act.f)
    f.is_action = True
    functions_core.register.append(f)


@Function(['w', 'weather'])
def displayweather(args, source, target):
    """displays the weather of the specified location"""
    print(' '.join(args))
    if args is None:
        yield 'please specify a location'
        stop()
    location = ' '.join(args).strip()
    r = weather.weatherget(location)
    yield '{color.bold}Température{color.reset}: {0} (min: {1}/max: {2})\n' \
          '{color.bold}Vent{color.reset}: {3} (direction {4})\n{color.bold}Taux d\'' \
          'humidité{color.resetreset}: {5} ({6} de précipitations)'.format(r.averagetemp,
                                                                           r.mintemp,
                                                                           r.maxtemp,
                                                                           r.windspeed,
                                                                           r.winddir,
                                                                           r.humidity,
                                                                           r.precipmm)


@Function('rot13')
def rot13(args, source, target):
    """Encrypt a text using ROT13 (http://en.wikipedia.org/wiki/ROT13), this only works with English; I'll be""" \
    """making the one for French, Spanish, Greek and many other languages with Abjad writing that I'm interested in."""
    yield codecs.encode(' '.join(args), 'rot-13')

