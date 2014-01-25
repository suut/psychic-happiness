# -*- coding: utf-8 -*-

import configparser, google, random, hashlib

actionsparser = configparser.ConfigParser()
actionsparser.read('strings/actions.ini') # to use the actions commands, like nommin or stuff

with open('strings/8ball.txt') as file:
    eightball_answers = file.read().split('\n') # for the 8ball command

with open('strings/abuse.txt') as file: # for the flame command
    flame_strs = file.read().split('\n')

with open('strings/quotes.txt') as file:
    quote_strs = file.read().split('\n')

with open('strings/fortunes.txt') as file:
    fortune_strs = file.read().split('\n')

with open('strings/insults.txt') as file:
    insult_strs = file.read().split('\n')

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
    def add_one(self, serv, bot, event, args):
        """action, use -list to list current people and -clear to clear the list out"""
        if args is not None and args[0] == '-list':
            if len(self.ppl) == 0:
                return 'Nobody!'
        elif args is not None and args[0] == '-clear':
            self.ppl = []
            return 'Ok...'
        elif event.source.nick not in self.ppl:
            self.ppl.append(event.source.nick)
        if len(self.ppl) > 1:
            return self.desc_several.format(names=type(self).sep(self.ppl))
        else:
            return self.desc_alone.format(name=self.ppl[0])

actions = {}

raw_actions = actionsparser['actions']

for k, v in zip(raw_actions.keys(), raw_actions.values()):
    action = Action(*v.split(';'))
    actions[k] = action

def eightball(serv, bot, event, args):
    """will answer your deepest questions"""
    if args is not None:
        seed = hash(' '.join(args).strip())
        return eightball_answers[seed%len(eightball_answers)]
    else:
        return 'What?'

def reverse(serv, bot, event, args):
    """returns the reversed representation of a string"""
    if args is not None:
        return ''.join(reversed(' '.join(args))).strip()

def utf8(serv, bot, event, args):
    """some kind of way to test if UTF-8 is functionning correctly"""
    return 'На берегу пустынных волн'

def search(serv, bot, event, args):
    """performs a google search and return the 1st result"""
    if args is not None:
        q = google.SearchQuery(' '.join(args))
        try:
            r = google.query(q)
        except BaseException as e:
            return 'No result found.'
        return r.display()
    else:
        return 'No query specified.'

def shorten(serv, bot, event, args):
    """shorten an url"""
    if args is not None:
        return google.shortenUrl(' '.join(args))
    else:
        return 'No URL specified.'

def expand(serv, bot, event, args):
    """expands a shortened url"""
    if args is not None:
        return google.expandUrl(' '.join(args))
    else:
        return 'No URL specified.'

def sha1(serv, bot, event, args):
    """hash a string with the SHA-1 algorithm"""
    if args is not None:
        return hashlib.sha1(' '.join(args).encode('UTF-8')).hexdigest()

def ping(serv, bot, event, args):
    """just try it"""
    return 'pong'

def masshl(serv, bot, event, args):
    """boom!"""
    return ' '.join(bot.channels[event.target].users())

def flame(serv, bot, event, args):
    """somebody did something wrong? flame him/her!"""
    if args is not None:
        serv.action(event.target, flame_strs[random.randrange(0, len(flame_strs))].format(user=' '.join(args).strip()))
    else:
        return 'Fuck off, little guy.'

def quote(serv, bot, event, args):
    """quotes from great men"""
    return quote_strs[random.randrange(0, len(quote_strs))]

def blabla(serv, bot, event, args):
    """1024*'o'"""
    return 1024*'o'

def fortune(serv, bot, event, args):
    """like in the cookies!"""
    return fortune_strs[random.randrange(0, len(fortune_strs))]

def insult(serv, bot, event, args):
    """fuck you"""
    return insult_strs[random.randrange(0, len(insult_strs))]

##############################
# NO DEFINE BELOW THIS POINT #
##############################

binding = {'reverse':   reverse,
           'utf8': utf8,
           'google': search,
           '8ball': eightball,
           'shorten': shorten,
           'expand': expand,
           'sha1': sha1,
           'ping': ping,
           'masshl': masshl,
           'flame': flame,
           'quote': quote,
           'blabla': blabla,
           'fortunes': fortune,
           'insult': insult}

for k, v in zip(actions.keys(), actions.values()):
    binding[k] = v.add_one

def doc(serv, bot, event, args): # defining it later because we need the binding dict
    """provides help for fantasy commands"""
    if args is None or ''.join(args).strip() == '':
        return 'Available fantasy commands: {0}\ntype {1}help <command> to know more about a specific command.' .format(', '.join(binding.keys()), bot.cmdprefix)
    else:
        cmdname = ''.join(args)
        if cmdname in binding:
            return binding[cmdname].__doc__
        else:
            return 'Command does not exist.'

binding['help'] = doc
