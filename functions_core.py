# -*- coding: utf-8 -*-

# functions_core.py
# Elements:
#       [X] IRC exceptions
#       [X] sandbox function
#       [X] function object

import core
from time import time
from auth_core import require, getinfos
import async_core


class IRCException(Exception):
    pass


class InvalidPasswordException(IRCException):
    pass


class NotSufficentPrivilegesException(IRCException):
    pass


class MutedCommandException(IRCException):
    pass


class MutedUserException(IRCException):
    pass


class UnknownCommandException(IRCException):
    pass


class InvalidArgumentsException(IRCException):
    pass


def sandbox(func):
    def f(*args, **kwargs):
        # args[0] is args
        # args[1] is source
        # args[2] is target
        try:
            ret = func(*args, **kwargs)
        except BaseException as e:
            print('{0}({1})'.format(str(e.__class__)[8:-2], ', '.join(repr(i) for i in e.args)))
            return 'an exception has occured: {0} (with arg(s): {1})'.format(str(e.__class__)[8:-2], ', '.join(repr(i) for i in e.args))
        return ret
    return f


class _Function:
    def __init__(self, cmdname, authlvl, requestserv, requestchans, f, doc):
        self.f = f
        self.cmdname = cmdname
        self.muted = False
        self.muted_users = []
        self.authlvl = authlvl
        self.requestserv = requestserv
        self.requestchans = requestchans
        self.doc = doc
    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)


register = []


def Function(cmdname, authlvl='none', requestserv=False, requestchans=False):
    def decorator(f):
        doc = f.__doc__
        f = sandbox(f)
        func = _Function(cmdname, authlvl, requestserv, requestchans, f, doc)
        if func not in register:
            register.append(func)
        else:
            register.pop(register.index(func))
            register.append(func)
        return func
    return decorator


usedlast = {}

def okthrottle(userhost):
    if userhost in usedlast.keys():
        if round(time())-usedlast[userhost]['timestamp'] < int(core.details['throttle']):
            if getinfos(userhost) is not None:
                #if the user is authed
                return 'ok'
            if not usedlast[userhost]['notified']:
                usedlast[userhost]['notified'] = True
                return 'notify'
            else:
                return 'donothing'
    return 'ok'

def updatethrottle(userhost):
    usedlast[userhost] = {'timestamp': round(time()), 'notified': False}


def match(f, cmd):
    if isinstance(f.cmdname, list):
        return cmd in f.cmdname
    else:
        return f.cmdname == cmd




def process_cmd(msg, source, target, serv, channels, callback):
    # [ ] check if the user is muted
    # [X] retrieve function registry
    # [X] get matching cmdnames
    if msg[0] in core.server_config['commands']['cmdprefix'] and len(msg) > 1:
        msg = msg[1:].split()
        cmd = msg[0].lower()
        args = None
        if len(msg) > 1:
            args = msg[1:]
        for f in register:
            if match(f, cmd):
                print('`{0}` from {1}'.format(cmd, source))
                if f.authlvl != 'none':
                    print('\tthis function requires {0} authlvl'.format(f.authlvl))
                    r = require(source, f.authlvl)
                    if r is not None:
                        serv.notice(source.nick, r)
                        return
                #it's a normal command, let's check if the throttle has ended
                if cmd.muted:
                r = okthrottle(source)
                if r == 'ok':
                    updatethrottle(source)
                    if f.requestchans and f.requestserv:
                        _args = (args, source, target, serv, channels)
                    elif f.requestserv:
                        _args = (args, source, target, serv)
                    elif f.requestchans:
                        _args = (args, source, target, channels)
                    else:
                        #NORMAL CASE
                        _args = (args, source, target)
                    thread = async_core.ControlThread(f, callback, *_args)
                    thread.start()
                    return
                elif r == 'notify':
                    serv.notice(source.nick, 'please wait at least {0} secondes between commands'.format(core.details['throttle']))
                    return
                elif r == 'donothing':
                    return
        #now let's verify if it's a trigger
        if cmd in core.triggers.keys():
            callback(core.triggers[cmd].format().replace('\\n', '\n'))
        return False


def process_privmsg(msg, source, serv, channels, callback):
    # [ ] check if the user is muted
    # [X] retrieve function registry
    # [X] get matching cmdnames
    msg = msg.split()
    cmd = msg[0].lower()
    args = None
    if len(msg) > 1:
        args = msg[1:]
    for f in register:
        if match(f, cmd):
            print('`{0}` from {1}'.format(cmd, source))
            if f.authlvl != 'none':
                print('this function requires {0} authlvl'.format(f.authlvl))
                r = require(source, f.authlvl)
                if r is not None:
                    serv.notice(source.nick, r)
                    return
            if f.requestserv and f.requestchans:
                _args = (args, source, source.nick, serv, channels)
            elif f.requestserv:
                _args = (args, source, source.nick, serv)
            elif f.requestchans:
                _args = (args, source, source.nick, channels)
            else:
                _args = (args, source, source.nick)
            thread = async_core.ControlThread(f, callback, *_args)
            thread.start()
