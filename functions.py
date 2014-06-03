#!/usr/bin/python3.2
# -*- coding: utf-8 -*-

from functions_core import Function, register
from core import server_config, format, version
from random import sample
import datetime
import google

@Function('ping')
def ping(args, source, target):
    """pong!"""
    return 'pong'

with open('eloges.txt') as file:
    sarah_adjs = file.read().split('\n')

with open('adjs.txt') as file:
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


@Function('g')
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


@Function('yt')
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


with open('pornos.txt') as file:
    pornos = file.read().split('\n')

@Function('film')
def film(args, source, target):
    """un nom de "film" au hasard"""
    return sample(pornos, 1)[0]


@Function('help')
def help(args, source, target):
    """provides help on commands"""
    if args is None: #showing all functions
        return 'commands are: {0}\nto know more about a particular command type {1}help cmdname'.format(', '.join(i.cmdname for i in register), server_config['commands']['cmdprefix'])
    elif len(args) != 1:
        return 'syntax is cmdname'
    else:
        for i in register:
            if i.cmdname == args[0].lower():
                if i.doc is None:
                    return 'command has no documentation yet'
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


with open('drugs.txt') as file:
    list_drugs = file.read().split('\n')

@Function('dotd')
def dotd(args, source, target):
    """drug of the day :)"""
    seed = int('{0}{1}{2}'.format(datetime.datetime.today().day, datetime.datetime.today().month, datetime.datetime.today().year))
    return '{0}drug of the day{1}: {2}'.format(format['bold'],
                                               format['reset'],
                                               list_drugs[seed%len(list_drugs)])

@Function('lapin')
def lapin(args, source, target):
    """lapin!!"""
    return 'celui qui a une grande..paire d\'oreilles'
