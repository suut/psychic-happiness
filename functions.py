#!/usr/bin/python3.2
# -*- coding: utf-8 -*-

from functions_core import Function, register
from core import ToSend, server_config, format
from random import sample
import google

@Function('ping')
def ping(args, source, target):
    """pong!"""
    return ToSend(target, 'pong')

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
    return ToSend(target, 'la plus {0}'.format(sample(sarah_adjs, 1)[0]))

@Function('hatsu')
def hatsu(args, source, target):
    """vous dira qui est-ce... :)"""
    return ToSend(target, 'la plus {0}'.format(sample(hatsu_adjs, 1)[0]))

@Function('test')
def test(args, source, target):
    """for testing purposes"""
    if args is not None:
        return ToSend(target, 'arguments provided: {0}; by {1} on {2}'.format(', '.join(args), source, target))
    else:
        return ToSend(target, 'it\'s ok')

@Function('eyecancer')
def eyecancer(args, source, target):
    """just try it :)"""
    return ToSend(target, '13,10UNTZ2,3UNTZ2,7UNTZ2,7UNTZ6,13UNTZ12,5UNTZ4,10UNTZ11,6UNTZ9,13UNTZ4,13UNTZ3,11UNTZ3,7UNTZ7,9UNTZ6,10UNTZ9,2UNTZ10,9UNTZ10,7UNTZ4,11UNTZ3,13UNTZ12,11UNTZ9,6UNTZ2,11UNTZ13,7UNTZ3,9UNTZ13,10UNTZ2,10UNTZ8,2UNTZ10,5UNTZ9,10UNTZ9,4UNTZ6,4UNTZ6,9UNTZ7,8UNTZ8,13UNTZ5,11UNTZ10,5UNTZ8,10UNTZ5,10UNTZ2,7UNTZ12,8UNTZ2,8UNTZ9,12UNTZ4,10UNTZ6,3UNTZ2,6UNTZ11,6UNTZ5,13UNTZ8,3UNTZ11,4UNTZ2,11UNTZ6,7UNTZ')

@Function('g')
def search(args, source, target):
    """performs a search via Google"""
    if args is not None:
        q = google.SearchQuery(' '.join(args))
        try:
            r = google.query(q)
        except IndexError as e:
            return ToSend(target, 'no results')
        else:
            return ToSend(target, r.display())
    return ToSend(target, 'no query specified')

@Function('yt')
def youtube(args, source, target):
    """performs a search on YouTube"""
    if args is not None:
        q = google.YoutubeQuery(' '.join(args))
        try:
            r = google.ytquery(q)
        except IndexError as e:
            return ToSend(target, 'no results')
        else:
            return ToSend(target, r.display())
    return ToSend(target, 'no query specified')

@Function('multilinetest')
def multilinetest(args, source, target):
    """a function to test multiline-msg cutting"""
    return ToSend(target, 'a\nb\nc')

with open('pornos.txt') as file:
    pornos = file.read().split('\n')

@Function('film')
def film(args, source, target):
    """un nom de "film" au hasard"""
    return ToSend(target, sample(pornos, 1)[0])

@Function('help')
def help(args, source, target):
    """provides help on commands"""
    if args is None: #showing all functions
        return ToSend(target, 'commands are: {0}\nto know more about a particular command type {1}help cmdname'.format(', '.join(i.cmdname for i in register), server_config['commands']['cmdprefix']))
    elif len(args) != 1:
        return ToSend(target, 'syntax is cmdname')
    else:
        for i in register:
            if i.cmdname == args[0].lower():
                if i.doc is None:
                    return ToSend(target, 'command has no documentation yet')
                else:
                    return ToSend(target, '{0}{1}{2}: {3}'.format(format['bold'], args[0].lower(), format['reset'], i.doc))
        return ToSend(target, 'unknown command "{0}"'.format(args[0].lower()))

@Function('quisuisje')
def quisuisje(args, source, target):
    """détermine avec exactitude qui vous êtes, ou plutôt ce que vous êtes"""
    return ToSend(target, 'vous êtes plutôt...{0}'.format(adjs[hash(source.nick )%len(adjs)]))

@Function('drugs')
def drugs(args, source, target):
    """provides a list of RC shops"""
    if target == '#psychonautfr':
        return ToSend(target, 'what the hell do you think you\'re doing??')
    else:
        return ToSend(target, 'http://nicolodouma.mooo.com/rc.html http://rcshops.pastebay.net/1279926')

@Function('error')
def error(args, source, target):
    """to test handling of exceptions"""
    raise RuntimeError('FATAL ERROR')
