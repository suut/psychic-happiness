#!/usr/bin/python3.2
# -*- coding: utf-8 -*-

# Differents auth level:
#   * master
#   * admin
#   * known

import configparser


class LoggedIn:
    def __init__(self, uname, host):
        self.uname = uname
        self.host = host

loggedin = []


uparser = configparser.ConfigParser()
uparser.read('config/users.ini')

userlist = uparser.sections()
print('registered users:', ', '.join(userlist))


def getinfos(host):
    # returns either None (not logged in), either the lvl
    for i in loggedin:
        if i.host == host:
            return {'uname': i.uname, 'level': uparser[i.uname]['level']}


def require(source, level):
    #used to protect a command from being used by everyone
    infos = getinfos(source)
    if level == 'known':
        levels = ('master', 'admin', 'known')
    elif level == 'admin':
        levels = ('admin', 'master')
    elif level == 'master':
        levels = ('master',)
    if infos is None or infos['level'] not in levels:
        return 'you\'re not authorized to use this command (need at least {0})'.format(level)
