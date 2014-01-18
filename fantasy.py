# -*- coding: utf-8 -*-

import configparser, google, random, hashlib

confparser = configparser.ConfigParser()
confparser.read('config.ini')

"""
fantasy protocol:
    def ...(source, args):
        ...
        return value_that_will_be_printed_to_channel
"""

eightball_answers = confparser['8ball']['answers'].split('\n')

class Action:
    def __init__(self, desc_alone, desc_several):
        self.desc_alone = desc_alone
        self.desc_several = desc_several
        self.ppl = []
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
    def add_one(self, source, args):
        """action"""
        if source.nick not in self.ppl:
            self.ppl.append(source.nick)
        if len(self.ppl) > 1:
            return self.desc_several.format(names=type(self).sep(self.ppl))
        else:
            return self.desc_alone.format(name=source.nick)
    def rem_one(self, source, args):
        if nick in self.ppl:
            self.ppl.remove(nick)

actions = {}

raw_actions = confparser['actions']

for k, v in zip(raw_actions.keys(), raw_actions.values()):
    action = Action(*v.split(';'))
    actions[k] = action

def eightball(source, args):
    """will answer your deepest questions"""
    seed = hash(' '.join(args).strip())
    return eightball_answers[seed%len(eightball_answers)]

def reverse(source, args):
    """returns the reversed representation of a string"""
    if args is not None:
        return ''.join(reversed(' '.join(args))).strip()

def utf8(source, args):
    """some kind of way to test if UTF-8 is functionning correctly"""
    return 'На берегу пустынных волн'

def search(source, args):
    """performs a google search and return the 1st result"""
    if args is not None:
        q = google.SearchQuery(' '.join(args))
        try:
            r = google.query(q)
        except KeyError:
            return 'No result found.'
        return r.display()
    else:
        return 'No query specified.'

def shorten(source, args):
    """shorten an url"""
    if args is not None:
        return google.shortenUrl(' '.join(args))
    else:
        return 'No URL specified.'

def expand(source, args):
    """expands a shortened url"""
    if args is not None:
        return google.expandUrl(' '.join(args))
    else:
        return 'No URL specified.'

def sha1(source, args):
    """hash a string with the SHA-1 algorithm"""
    if args is not None:
        return hashlib.sha1(' '.join(args).encode('UTF-8')).hexdigest()

##############################
# NO DEFINE BELOW THIS POINT #
##############################

binding = {'reverse':   reverse,
           'utf8': utf8,
           'google': search,
           '8ball': eightball,
           'shorten': shorten,
           'expand': expand,
           'sha1': sha1}

for k, v in zip(actions.keys(), actions.values()):
    binding[k] = v.add_one

def doc(source, args): # defining it later because we need the binding dict
    """provides help for fantasy commands"""
    if args is None or ''.join(args).strip() == '':
        return 'Available fantasy commands: {0}\ntype {1}help <command> to know more about a specific command.' .format(', '.join(binding.keys()), confparser['bot']['cmdprefix'])
    else:
        cmdname = ''.join(args)
        if cmdname in binding:
            return binding[cmdname].__doc__
        else:
            return 'Command does not exist.'

binding['help'] = doc
