# -*- coding: utf-8 -*-

import hashlib, configparser
from util import Enum

"""
admnin protocol:
    def ...(serv, bot, source, args):
        ...
        return value_that_will_be_printed_to_channel
"""

encode_passwd = lambda s: hashlib.sha1(s.encode('UTF-8')).hexdigest()

users = configparser.ConfigParser()
users.read('users.ini')

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

def whoami(serv, bot, source, args):
    for i in logged_in:
        if source.userhost == i.userhost:
            ret = 'You\'re logged in.\n'
            if int(users[i.username]['privileges']) & privileges.master:
                ret += 'You\'re master.'
            elif int(users[i.username]['privileges']) & privileges.admin:
                ret += 'You\'re admin.'
            elif int(users[i.username]['privileges']) & privileges.known:
                ret += 'You\'re known.'
            return ret
    return 'You\'re nobody, lil boy.'

def auth(serv, bot, source, args):
    unpacked = ' '.join(args).strip().split(' ')
    if len(unpacked) != 2:
        return 'Invalid arguments. Usage: auth <username> <password>'
    username, password = unpacked
    if username not in users.sections():
        return 'Unknown username.'
    if users[username]['password'] != hashlib.sha1(password.encode('UTF-8')).hexdigest():
        return 'Invalid password.'
    logged_in.append(LoggedIn(source, username))
    return 'You\'re successfully logged in!'

def logout(serv, bot, source, args):
    for i in logged_in:
        if i.userhost == source.userhost:
            logged_in.remove(i)
            return 'Successfully logged out.'
    return 'You\'re not logged in.'

def die(serv, bot, source, args):
    for i in logged_in:
        if source.userhost == i.userhost:
            if int(users[i.username]['privileges']) & privileges.admin or int(users[i.username]['privileges']) & privileges.master:
                bot.disconnect('die command used by {0}'.format(source.nick))
            else:
                return 'Not sufficent privileges, need at least admin capabilities.'
    return 'You\'re not logged in.'

##############################
# NO DEFINE BELOW THIS POINT #
##############################

binding = {'whoami': whoami,
           'auth': auth,
           'logout': logout,
           'die': die}
