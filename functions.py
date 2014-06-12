#!/usr/bin/python3.2
# -*- coding: utf-8 -*-

from functions_core import Function, register, match, Function
from core import server_config, format, version
from random import sample
import datetime
import google
import soundcloud
import configparser
import weather

@Function('ping')
def ping(args, source, target):
    """pong!"""
    return 'pong'

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
 pas               'insalubre',
              'saccagée',
              'ravagée')


@Function('sarah')
def sarah(args, source, target):
    """vous dira qui est-ce... :)"""
    return 'la plus {0}'.format(sample(sarah_adjs, 1)[0])


@Function('hatsu', requestchans=True)
def hatsu(args, source, target, channels):
    """vous dira qui est-ce... :)"""
    if 'hatsu' not in channels[target].userdict.keys():
        return 'la plus {0}'.format(sample(hatsu_adjs, 1)[0])
    else:
        return 'la plus {0}'.format(sample(sarah_adjs, 1)[0])


@Function('eyecancer')
def eyecancer(args, source, target):
    """just try it :)"""
    return '13,10UNTZ2,3UNTZ2,7UNTZ2,7UNTZ6,13UNTZ12,5UNTZ4,10UNTZ11,6UNTZ9,13UNTZ4,13UNTZ3,11UNTZ3,7UNTZ7,9UNTZ6,10UNTZ9,2UNTZ10,9UNTZ10,7UNTZ4,11UNTZ3,13UNTZ12,11UNTZ9,6UNTZ2,11UNTZ13,7UNTZ3,9UNTZ13,10UNTZ2,10UNTZ8,2UNTZ10,5UNTZ9,10UNTZ9,4UNTZ6,4UNTZ6,9UNTZ7,8UNTZ8,13UNTZ5,11UNTZ10,5UNTZ8,10UNTZ5,10UNTZ2,7UNTZ12,8UNTZ2,8UNTZ9,12UNTZ4,10UNTZ6,3UNTZ2,6UNTZ11,6UNTZ5,13UNTZ8,3UNTZ11,4UNTZ2,11UNTZ6,7UNTZ'


@Function(['g', 'google'])
def search(args, source, target):
    """performs a search via Google"""
    if args is not None:
        q = google.SearchQuery(' '.join(args))
        try:
            r = google.query(q)
        except IndexError as e:
            return 'no results'
        else:
            return '{0}{1}{2} — {3}\n{4}\n{5}{6}{7}{8}'.format(format['bold'],
                                                               r.title,
                                                               format['reset'],
                                                               r.display_url,
                                                               r.abstract,
                                                               format['bold'],
                                                               format['underlined'],
                                                               r.link,
                                                               format['reset'])
    return 'no query specified'


@Function(['yt', 'youtube'])
def youtube(args, source, target):
    """performs a search on YouTube"""
    if args is not None:
        q = google.YoutubeQuery(' '.join(args))
        try:
            r = google.ytquery(q)
        except IndexError as e:
            return 'no results'
        else:
            return '{0}{1}{2} — {3}\n{4}\n{5}{6}http://youtu.be/{7}{8}'.format(format['bold'],
                                                                               r.title,
                                                                               format['reset'],
                                                                               r.channel,
                                                                               r.description,
                                                                               format['bold'],
                                                                               format['underlined'],
                                                                               r.id,
                                                                               format['reset'])
    return 'no query specified'


with open('strings/pornos.txt') as file:
    pornos = file.read().split('\n')

@Function('film')
def film(args, source, target):
    """un nom de "film" au hasard"""
    return sample(pornos, 1)[0]


@Function('help')
def help(args, source, target):
    """provides help on commands"""
    if args is None: #showing all functions
        list_of_cmds = []
        for f in register:
            if isinstance(f.cmdname, list):
                list_of_cmds.append(' = '.join(f.cmdname))
            else:
                if 'is_action' not in dir(f):
                    list_of_cmds.append(f.cmdname)
        return 'commands are: {0}\nto know more about a particular command type {1}help cmdname'.format(', '.join(list_of_cmds), server_config['commands']['cmdprefix'])
    elif len(args) != 1:
        return 'syntax is cmdname'
    else:
        for i in register:
            if match(i, args[0].lower()):
                if i.doc is None:
                    return 'command has no documentation'
                else:
                    return '{0}{1}{2}: {3}'.format(format['bold'], args[0].lower(), format['reset'], i.doc)
        return 'unknown command "{0}"'.format(args[0].lower())


@Function('quisuisje')
def quisuisje(args, source, target):
    """détermine avec exactitude qui vous êtes, ou plutôt ce que vous êtes"""
    return 'vous êtes plutôt...{0}'.format(adjs[hash(source.nick )%len(adjs)])


@Function('drugs')
def drugs(args, source, target):
    """provides a list of RC shops"""
    if target == '#psychonautfr':
        return 'what the hell do you think you\'re doing??'
    else:
        return 'http://rcshops.pastebay.net/1279926'


@Function('error')
def error(args, source, target):
    """to test handling of exceptions"""
    raise RuntimeError('FATAL ERROR')


@Function('source')
def source(args, source, target):
    """prints the URL of the source code (on github)"""
    return '{0}source code{1}: https://github.com/suut/psychic-happiness/tree/v2/'.format(format['bold'], format['reset'])


@Function('version')
def version_(args, source, target):
    """prints the actual bot version"""
    return version


with open('strings/drugs.txt') as file:
    list_drugs = file.read().split('\n')

@Function('dotd')
def dotd(args, source, target):
    """drug of the day :)"""
    seed = int('{0}{1}'.format(datetime.datetime.today().month, datetime.datetime.today().day))
    return '{0}drug of the day{1}: {2}'.format(format['bold'],
                                               format['reset'],
                                               list_drugs[seed%len(list_drugs)])


@Function('lapin')
def lapin(args, source, target):
    """lapin!!"""
    return 'celui qui a une grande..paire d\'oreilles'


@Function('rainbow')
def rainbow(args, source, target):
    """a 'rainbow'"""
    return '04,04...07,07...08,08...03,03...02,02...13,13...06,06...\n04,04...07,07...08,08...03,03...02,02...13,13...06,06...\n04,04...07,07...08,08...03,03...02,02...13,13...06,06...'


@Function(['sc', 'soundcloud'])
def scsearch(args, source, target):
    """performs a search on soundcloud"""
    if args is not None:
        r = soundcloud.soundcloud_search(' '.join(args))
        if r is None:
            return 'no results'
        return '{0}{1}{2} — {3}\n{4}\n{5}{6}{7}{8}'.format(format['bold'],
                                                           r['title'],
                                                           format['reset'],
                                                           r['username'],
                                                           r['description'].replace('\n', '').replace('\r', '')[:400],
                                                           format['underlined'],
                                                           format['bold'],
                                                           r['url'],
                                                           format['reset'])
    else:
        return 'no query specified'


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
            return 'nobody {0} anymore? :('.format(self.name)
        if len(self.ppl) == 0:
            self.ppl.append(source.nick)
            return self.one_f(source.nick)
        else:
            if source.nick not in self.ppl:
                self.ppl.append(source.nick)
            if len(self.ppl) == 1:
                #just display the list
                return self.one_f(self.ppl[0])
            else:
                return self.many_f(self.ppl)

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
    register.append(f)

@Function(['w', 'weather'])
def displayweather(args, source, target):
    if args is None:
        return 'please specify a location'
    location = ' '.join(args).strip()
    r = weather.weatherget(location)
    return '{bold}Température{reset}: {0} (min: {1}/max: {2})\n' \
           '{bold}Vent{reset}: {3} (direction {4})\n{bold}Taux d\'' \
           'humidité{reset}: {5} ({6} de précipitations)'.format(r.averagetemp,
                                                          r.mintemp,
                                                          r.maxtemp,
                                                          r.windspeed,
                                                          r.winddir,
                                                          r.humidity,
                                                          r.precipmm,
                                                          bold=format['bold'],
                                                          reset=format['reset'])
