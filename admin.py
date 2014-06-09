#!/usr/bin/python3.2
# -*- coding: utf-8 -*-

# Differents auth level:
#   * master
#   * admin
#   * known

from functions_core import Function
import hashlib
from auth_core import uparser, loggedin, LoggedIn, getinfos, require
from core import server_config, write_config, format


@Function('auth', requestserv=True)
def auth(args, source, target, serv):
    # args should be (username, password)
    if args is None or len(args) < 2:
        serv.notice(source.nick, 'usage: AUTH username password')
        return
    if args[0] not in uparser.sections():
        serv.notice(source.nick, 'unknown user')
        return
    if hashlib.sha1(args[1].encode()).hexdigest() != uparser[args[0]]['password']:
        serv.notice(source.nick, 'invalid password')
        return
    for user in loggedin:
        if user.host == source.userhost:
            serv.notice(source.nick, 'you\'re already logged in')
            return
    loggedin.append(LoggedIn(' '.join(args).strip(), source.userhost))
    serv.notice(source.nick, 'you\'re now logged in')


@Function('whoami')
def whoami(args, source, target):
    ret = getinfos(source.userhost)
    if ret is None and source.nick.lower() == 'sarah':
        return 'you\'re the most beautiful one'
    #TODO: to remove one day
    if ret is None:
        return 'you\'re nobody'
    return 'you\'re {0} ({1})'.format(ret['uname'], ret['level'])

@Function('say', requestserv=True, authlvl='known')
def say(args, source, target, serv):
    r = require(source, 'known')
    if r is not None:
        return r
    # args should be (chan, text)
    if args is None or len(args) < 2:
        serv.notice(source.nick, 'args should be (chan, text)')
        return
    serv.privmsg(args[0], ' '.join(args[1:]))

@Function('act', requestserv=True, authlvl='known')
def act(args, source, target, serv):
    # args should be (chan, text)
    if args is None or len(args) < 2:
        serv.notice(source.nick, 'args should be (chan, text)')
        return
    serv.action(args[0], ' '.join(args[1:]))

@Function('nick', requestserv=True, authlvl='master')
def nick(args, source, target, serv):
    if args is None or len(args) != 1:
        serv.notice(source.nick, 'args should be newnickname')
        return
    serv.nick(args[0])

@Function('join', requestserv=True, authlvl='admin')
def join(args, source, target, serv):
    if args is None or len(args) != 1:
        serv.notice(source.nick, 'args should be channel')
        return
    serv.join(args[0])

@Function('part', requestserv=True, authlvl='admin')
def part(args, source, target, serv):
    if target[0] == '#':
        if args is None:
            serv.part(target, 'bye')
        elif len(args) == 1 and args[0][0] == '#':
            serv.part(args[0], 'bye')
        elif len(args) == 1 and args[0][0] != '#':
            serv.part(target, args[0])
        elif len(args) > 1 and args[0][0] == '#':
            serv.part(args[0], ' '.join(args[1:]))
        elif len(args) > 1 and args[0][0] != '#':
            serv.part(target, ' '.join(args))
    else:
        if args is None:
            serv.notice(target, 'invalid syntax')
            return
        elif len(args) == 1 and args[0][0] == '#':
            serv.part(args[0], 'bye')
        elif len(args) > 1 and args[0][0] == '#':
            serv.part(args[0], ' '.join(args[1:]))
        else:
            serv.notice(source.nick, 'invalid syntax')
            return

@Function('die', requestserv=True, authlvl='master')
def die(args, source, target, serv):
    if args is None:
        serv.quit('bye')
        quit(0)
    else:
        serv.quit(' '.join(args))
        quit(0)

@Function('notice', requestserv=True, authlvl='known')
def notice(args, source, target, serv):
    if args is None or len(args) < 2:
        serv.notice(source.nick, 'args should be (target, text)')
        return
    else:
        serv.notice(args[0], ' '.join(args[1:]))

@Function('throttle', authlvl='admin')
def throttle(args, source, target):
    if args is not None:
        if ''.join(args).isdigit():
            server_config['details']['throttle'] = ''.join(args)
            return 'throttle set to {0}'.format(''.join(args))
        else:
            return 'usage: THROTTLE time'
    else:
        return 'throttle actually set to {0}'.format(server_config['details']['throttle'])


@Function('saveconfig', requestchans=True, requestserv=True, authlvl='master')
def saveconfig(args, source, target, serv, channels):
    chans = ','.join(channels.keys())
    server_config['details']['channels'] = chans
    server_config['details']['nickname'] = serv.get_nickname()
    write_config()
    return 'config writed successfully. {0}channels{1}: {2}; {0}nickname{1}: {3}; {0}throttle{1}: {4}'.format(format['bold'],
                                                                                                              format['reset'],
                                                                                                              chans,
                                                                                                              serv.get_nickname(),
                                                                                                              serv['details']['throttle'])
