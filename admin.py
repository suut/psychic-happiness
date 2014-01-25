# -*- coding: utf-8 -*-

import hashlib, configparser
from util import Enum

"""
admnin protocol:
    def ...(serv, bot, event, args):
        ...
        return value_that_will_be_printed_to_channel
"""

encode_passwd = lambda s: hashlib.sha1(s.encode('UTF-8')).hexdigest()

users = configparser.ConfigParser()
users.read('config/users.ini')

privileges = Enum({'known':  1<<0,
                   'master': 1<<1,
                   'admin':  1<<2})

class LoggedIn:
    def __init__(self, nickmask, username):
        self.nickmask = nickmask
        self.username = username
    @property
    def nick(self):
        return self.nickmask.nick
    @property
    def userhost(self):
        return self.nickmask.userhost
    @property
    def host(self):
        return self.nickmask.host
    @property
    def user(self):
        return self.nickmask.user

logged_in = []

def is_logged_in(userhost):
    for i in logged_in:
        if i.userhost == userhost:
            return True
    return False

def get_login(userhost):
    for i in logged_in:
        if i.userhost == userhost:
            return i
    return None

######################
# BEGGINING COMMANDS #
######################

def whoami(serv, bot, event, args):
    if is_logged_in(event.source.userhost):
        ret = 'You\'re logged in.\n'
        if int(users[get_login(event.source.userhost).username]['privileges']) & privileges.master:
            ret += 'You\'re master.'
        elif int(users[get_login(event.source.userhost).username]['privileges']) & privileges.admin:
            ret += 'You\'re admin.'
        elif int(users[get_login(event.source.userhost).username]['privileges']) & privileges.known:
            ret += 'You\'re known.'
        return ret
    return 'You\'re nobody, lil boy.'

def auth(serv, bot, event, args):
    unpacked = ' '.join(args).strip().split(' ')
    if len(unpacked) != 2:
        return 'Invalid arguments. Usage: auth <username> <password>'
    username, password = unpacked
    if username not in users.sections():
        return 'Unknown username.'
    if users[username]['password'] != hashlib.sha1(password.encode('UTF-8')).hexdigest():
        return 'Invalid password.'
    logged_in.append(LoggedIn(event.source, username))
    return 'You\'re successfully logged in!'

def logout(serv, bot, event, args):
    if is_logged_in(event.source.userhost):
        logged_in.remove(get_login(event.source.userhost))
        return 'Successfully logged out.'
    return 'You\'re not logged in.'

def die(serv, bot, event, args):
    if is_logged_in(event.source.userhost):
        if int(users[get_login(event.source.userhost).username]['privileges']) & privileges.admin or int(users[get_login(event.source.userhost).username]['privileges']) & privileges.master:
            bot.disconnect('die command used by {0}'.format(event.source.nick))
            exit(0)
        else:
            return 'Not sufficent privileges, need at least admin capabilities.'
    return 'You\'re not logged in.'

def join(serv, bot, event, args):
    if is_logged_in(event.source.userhost):
        if int(users[get_login(event.source.userhost).username]['privileges']) & privileges.admin or int(users[get_login(event.source.userhost).username]['privileges']) & privileges.master or int(users[get_login(event.source.userhost).username]['privileges']) & privileges.known:
            if args is not None:
                for chan in ''.join(args).split(','):
                    serv.join(chan)
            else:
                for chan in bot._channels:
                    serv.join(chan)
                return 'No channel specified, joining default channels'
        else:
            return 'Not sufficent privileges, need at least known capabilities.'
    else:
        return 'You\'re not logged in.'

def part(serv, bot, event, args):
    if is_logged_in(event.source.userhost):
        if int(users[get_login(event.source.userhost).username]['privileges']) & privileges.admin or int(users[get_login(event.source.userhost).username]['privileges']):
            if args is not None:
                serv.part(''.join(args), 'part command used by {0}'.format(event.source.nick))
            else:
                serv.part(event.target, 'part command used by {0}'.format(event.source.nick))
        else:
            return 'Not sufficent privileges, need at least admin capabilities.'
    else:
        return 'You\'re not logged in.'

##############################
# NO DEFINE BELOW THIS POINT #
##############################

binding = {'whoami': whoami,
           'auth': auth,
           'logout': logout,
           'die': die,
           'join': join,
           'part': part}
