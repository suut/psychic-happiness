#!/usr/bin/python3.2
# -*- coding: utf-8 -*-

# Differents auth level:
#   * master
#   * admin
#   * known

from functions_core import Function
import functions_core
import hashlib
import auth_core
from core import server_config, write_config, stop, triggers, savetriggers
import sys
import format


@Function('auth', requestserv=True)
def auth(args, source, target, serv):
    # args should be (username, password)
    if args is None or len(args) < 2:
        serv.notice(source.nick, 'usage: AUTH username password')
        return
    if args[0] not in auth_core.uparser.sections():
        serv.notice(source.nick, 'unknown user')
        return
    if hashlib.sha1(' '.join(args[1:]).strip().encode()).hexdigest() != auth_core.uparser[args[0]]['password']:
        serv.notice(source.nick, 'invalid password')
        return
    for user in auth_core.loggedin:
        if user.host == source:
            serv.notice(source.nick, 'you\'re already logged in')
            return
    auth_core.loggedin.append(auth_core.LoggedIn(args[0], source))
    serv.notice(source.nick, 'you\'re now logged in')


@Function('whoami')
def whoami(args, source, target):
    ret = auth_core.getinfos(source)
    if ret is None and source.nick.lower() == 'sarah':
        yield 'you\'re the most beautiful one'
    #TODO: to remove one day
    if ret is None:
        yield 'you\'re nobody'
        stop()
    yield 'you\'re {0} ({1})'.format(ret['uname'], ret['level'])

@Function('say', requestserv=True)
def say(args, source, target, serv):
    # args should be (chan, text)
    if args is not None and target[0] == '#' and args[0][0] != '#':
        yield ' '.join(args).format(color=format.color)
        stop()
    if args is None or len(args) < 2:
        serv.notice(source.nick, 'args should be (chan, text)')
        stop()
    serv.privmsg(args[0], ' '.join(args[1:]).format(color=format.color))

@Function('act', requestserv=True)
def act(args, source, target, serv):
    # args should be (chan, text)
    if args is not None and target[0] == '#' and args[0][0] != '#':
        serv.action(target, ' '.join(args).format(color=format.color))
        return
    if args is None or len(args) < 2:
        serv.notice(source.nick, 'args should be (chan, text)')
        return
    serv.action(args[0], ' '.join(args[1:]).format(color=format.color))

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
        if '-restart' in args:
            args.remove('-restart')
            serv.quit('restarting')
        else:
            serv.quit(' '.join(args))
            sys.exit()

@Function('notice', requestserv=True, authlvl='known')
def notice(args, source, target, serv):
    if args is None or len(args) < 2:
        serv.notice(source.nick, 'args should be (target, text)')
        return
    else:
        serv.notice(args[0], ' '.join(args[1:]).format(color=format.color))

@Function('throttle', authlvl='admin')
def throttle(args, source, target):
    if args is not None:
        if ''.join(args).isdigit():
            server_config['details']['throttle'] = ''.join(args)
            yield 'throttle set to {0}'.format(''.join(args))
            stop()
        else:
            yield 'usage: THROTTLE time'
            stop()
    else:
        yield 'throttle actually set to {0}'.format(server_config['details']['throttle'])


@Function('saveconfig', requestchans=True, requestserv=True, authlvl='master')
def saveconfig(args, source, target, serv, channels):
    chans = ','.join(channels.keys())
    server_config['details']['channels'] = chans
    server_config['details']['nickname'] = serv.get_nickname()
    write_config()
    savetriggers()
    yield 'config writed successfully. {color.bold}channels{color.reset}: {}; {color.bold}nickname{color.reset}: {}; {color.bold}throttle{color.reset}: {}'.format(chans,
                                                                                                                                              serv.get_nickname(),
                                                                                                                                              server_config['details']['throttle'])

@Function('showconfig')
def showconfig(args, source, target):
    """shows the current configuration"""
    yield '{color.bold}channels{color.reset}: {}; {color.bold}nickname{color.reset}: {}; {color.bold}throttle{color.reset}: {}'.format(server_config['details']['channels'],
                                                                                                                                       server_config['details']['nickname'],
                                                                                                                                       server_config['details']['throttle'])


@Function('addtrigger')
def addtrigger(args, source, target):
    """add a trigger"""
    if args is None or len(args) < 2:
        yield 'syntax: ADDTRIGGER name text'
        stop()
    name, text = args[0], ' '.join(args[1:])
    triggers[name] = text
    yield 'trigger {} added for "{}"'.format(name, text)


@Function('deltrigger', authlvl='known')
def deltrigger(args, source, target):
    if args is None or len(args) != 1:
        yield 'syntax: DELTRIGGER name'
        stop()
    name = args[0]
    if name in triggers.keys():
        del triggers[name]
        yield 'trigger {} successfully deleted'.format(name)
        stop()
    else:
        yield 'trigger {} not found'.format(name)
        stop()


@Function('showtriggers')
def showtriggers(args, source, target):
    yield '{color.bold}triggers{color.reset}: {}'.format(', '.join(triggers.keys()))
