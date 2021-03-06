#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

#we need to do it from the outside for an evident reason..

#we need the strict minimum
from functions_core import Function
from core import reloadable_modules, stop
import importlib, functions, soundcloud, google, weather, parse_links, admin


confirmation = []
#if the list is empty, put (hostname, module) in the list, then calling reload -agree will do the job

@Function('reload', authlvl='master', requestserv=True)
def reloadcmds(args, source, target, serv):
    if args is not None and ''.join(args).strip() == '-list':
        yield '{0}04[EXPERIMENTAL]{1} following modules are reloadable: {2}\n' \
              'usage: -list to get this, -all to reload every module, -force ' \
              'to force reload any module (even unlisted), or specify a' \
              'particular module'.format(format['bold'],
                                         format['reset'],
                                         ' '.join(reloadable_modules))
        stop()

    if args is not None and ''.join(args).strip() == '-all':
        yield 'reloading {0}{1}every{2} module..'.format(format['bold'],
                                                         format['underlined'],
                                                         format['reset'])
        for i in (eval(j) for j in reloadable_modules):
            importlib.reload(i)
        yield 'done.'
        stop()

    if args is not None and '-force' in args:
        if len(args) != 2:
            yield 'usage: reload modulename -force'
            stop()
        args.remove('-force')
        for i in confirmation:
            if source == i[0]:
                yield 'you have to execute the command reload -agree'
                stop()
        confirmation.append((source, args[0]))
        yield '{bold}{underlined}04[VERY EXPERIMENTAL]{reset} now type' \
              ' the command reload -agree in order to reload module "{0}"' \
              ', or -cancel to cancel the query'.format(args[0],
                                                        bold=format['bold'],
                                                        underlined=format['underlined'],
                                                        reset=format['reset'])
        stop()

    if args is not None and ''.join(args).strip() == '-agree':
        for i in confirmation:
            if source == i[0]:
                yield 'trying to reload module "{0}"'.format(i[1])
                if i[1] not in dir():
                    yield 'importing it first..'
                    m = __import__(i[1])  # TODO: fix that thing
                else:
                    m = eval(i[0])
                importlib.reload(m)
                yield 'done.'
                stop()
        yield '?'
        stop()

    if args is not None and ''.join(args).strip() == '-cancel':
        for i in confirmation:
            if source == i[0]:
                confirmation.remove(i)
                yield 'done.'
                stop()
        yield '?'
        stop()

    if args is not None:
        mod = ''.join(args)
        if mod not in reloadable_modules:
            yield 'unknown/unreloadable module. maybe try -force?'
            stop()
        importlib.reload(eval(mod))
        yield 'reloaded module.'
        stop()

    else:
        importlib.reload(functions)
        yield 'functions reloaded successfully'
        stop()
