#!/usr/bin/python3.3
# -*- coding: utf-8 -*-

import irc.bot, parse_links
from functions_core import process_cmd, process_privmsg
from core import split, format
from auth_core import loggedin

class SuperBot(irc.bot.SingleServerIRCBot):
    def __init__(self, server):
        print('initializing...')
        super().__init__((server,), server.nickname, server.username, server.realname)
        self.connection.buffer_class.errors = 'replace' # prevents crashing due to unicode errors
        self._channels = server.channels
        self.modes = server.modes
        print('bot initialized.')

    def start(self):
        print('starting bot...')
        super().start()

    def on_welcome(self, serv, event):
        print('\tgot welcome message.')
        if self.modes != '':
            serv.mode(serv.get_nickname(), self.modes)
        if self._channels is not None:
            print('\tjoining following channels:', ', '.join(self._channels), '...')
            for chan in self._channels:
                serv.join(chan)
            print('\tchannel joining attempt done.')
        print('bot started.')
        print('nickname:', serv.get_nickname())

    def on_kick(self, serv, event):
        if event.arguments[0] == serv.get_nickname():
            serv.join(event.target)
            serv.privmsg(event.target, 'je t\'en foutrais moi du "{0}" pd de {1}'.format(event.arguments[1].strip(), event.source.nick))

    def on_pubmsg(self, serv, event):
        ret = process_cmd(event.arguments[0], event.source, event.target, serv, self.channels)
        if ret is not None:
            for i in split(ret, event.target):
                serv.privmsg(event.target, i)
        else:
            #it is not a command, let's verify if it contains links
            try:
                title = parse_links.parse(event.arguments[0])
            except Exception as e:
                pass
            else:
                if title is not None:
                    serv.privmsg(event.target, '{0}link{1}: {2}'.format(format['bold'],
                                                                                     format['reset'],
                                                                                     title.replace('\n', '')))

    def on_privmsg(self, serv, event):
        ret = process_privmsg(event.arguments[0], event.source, serv, self.channels)
        if ret is not None:
            for i in split(ret, event.source.nick):
                serv.privmsg(event.source.nick, i)

    def on_part(self, serv, event):
        #an user just parted
        #let's verify if (s)he's authed
        for i in loggedin:
            if i.host == event.source.userhost:
                #he was a logged in user
                #let's now check if he's on other common channels
                for name, chan in zip(self.channels.keys(), self.channels.values()):
                    if event.source.nick in chan.userdict.keys():
                        #phew! he's on another common channel
                        return
                #he's not on other channels, let's remove it
                loggedin.remove(i)

    def on_quit(self, serv, event):
        #an user just quitted
        #let's verify if (s)he's authed
        for i in loggedin:
            if i.host == event.source.userhost:
                #he was a logged in user
                loggedin.remove(i)

