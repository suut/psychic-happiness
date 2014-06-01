# -*- coding: utf-8 -*-

# functions_core.py
# Elements:
#       [X] IRC exceptions
#       [X] sandbox function
#       [X] function object

import core
from auth_core import require


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

# a function either sends NEXT to call the next function on the list either
# STOP, with argument what should be printed back on the channel, sent to a
# print_to_channel type of function


def sandbox(func):
    def f(*args, **kwargs):
        # args[0] is args
        # args[1] is source
        # args[2] is target
        try:
            ret = func(*args, **kwargs)
        except BaseException as e:
            print('{0}({1})'.format(str(e.__class__)[8:-2], ', '.join(repr(i) for i in e.args)))
            return core.ToSend(args[2], 'an exception has occured: {0} (with arg(s): {1})'.format(str(e.__class__)[8:-2], ', '.join(repr(i) for i in e.args)))
        return ret
    return f


class _Function:
    def __init__(self, cmdname, authlvl, requestserv, f, doc):
        self.f = f
        self.cmdname = cmdname
        self.muted = False
        self.muted_users = []
        self.authlvl = authlvl
        self.requestserv = requestserv
        self.doc = doc
    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)


register = []


def Function(cmdname, authlvl='none', requestserv=False):
    def decorator(f):
        doc = f.__doc__
        f = sandbox(f)
        func = _Function(cmdname, authlvl, requestserv, f, doc)
        register.append(func)
        return func
    return decorator


def process_cmd(msg, source, target, serv):
    # [ ] check if the user is muted
    # [X] retrieve function registry
    # [X] get matching cmdnames
    if msg[0] == core.server_config['commands']['cmdprefix'] and len(msg) > 1 and ''.join(set(msg.strip())) != core.server_config['commands']['cmdprefix']:
                                                                                    # allows to type e.g. "..."
        msg = msg[1:].split()
        cmd = msg[0].lower()
        args = None
        if len(msg) > 1:
            args = msg[1:]
        for f in register:
            if f.cmdname == cmd:
                print('`{0}` from {1}'.format(cmd, source))
                if f.authlvl != 'none':
                    print('\tthis function requires {0} authlvl'.format(f.authlvl))
                    r = require(source, f.authlvl)
                    if r is not None:
                        serv.notice(source.nick, r)
                        return
                if f.requestserv:
                    return f(args, source, target, serv)
                else:
                    return f(args, source, target)


def process_privmsg(msg, source, serv):
    # [ ] check if the user is muted
    # [X] retrieve function registry
    # [X] get matching cmdnames
    msg = msg.split()
    cmd = msg[0].lower()
    args = None
    if len(msg) > 1:
        args = msg[1:]
    for f in register:
        if f.cmdname == cmd:
            print('`{0}` from {1}'.format(cmd, source))
            if f.authlvl != 'none':
                print('this function requires {0} authlvl'.format(f.authlvl))
                r = require(source, f.authlvl)
                if r is not None:
                    serv.notice(source.nick, r)
                    return
            if f.requestserv:
                return f(args, source, source.nick, serv)
            else:
                return f(args, source, source.nick)

## EXEMPLE
##    @Function(cmdnames=('reverse',),)
##    def reverse(s):
##      return STOP(core.ToSend('#bite', s[::-1]))
