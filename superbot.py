#!/usr/bin/python3.3
# -*- coding: utf-8 -*-

import irc.bot, parse_links
from functions_core import process_cmd, process_privmsg

class SuperBot(irc.bot.SingleServerIRCBot):
    def __init__(self, server):
        print('initializing...')
        super().__init__((server,), server.nickname, server.username, server.realname)
        self.connection.buffer_class.errors = 'replace' # prevents crashing due to unicode errors
        self._channels = server.channels
        print('bot initialized.')

    def start(self):
        print('starting bot...')
        super().start()

    def on_welcome(self, serv, event):
        print('\tgot welcome message.')
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
        ret = process_cmd(event.arguments[0], event.source, event.target, serv)
        if ret is not None:
            for i in ret.content:
                serv.privmsg(ret.target, i)
        else:
            #it is not a command, let's verify if it contains links
            try:
                title = parse_links.parse(event.arguments[0])
            except Exception as e:
                pass
            else:
                if title is not None:
                    serv.privmsg(event.target, title.replace('\n', ''))

    def on_privmsg(self, serv, event):
        ret = process_privmsg(event.arguments[0], event.source, serv)
        if ret is not None:
            for i in ret.content:
                serv.privmsg(ret.target, i)
