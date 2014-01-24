# -*- coding: utf-8 -*-

import irc.bot, fantasy, admin
from util import unpack

class SpiderBot(irc.bot.SingleServerIRCBot):
    def __init__(self, server, channels, version, cmdprefix, adminprefix):
        super().__init__((server,), server.nickname, server.realname)
        self.connection.buffer_class.errors = 'replace' # prevents crashing due to unicode errors
        self._channels = channels
        self.version = version
        self.cmdprefix = cmdprefix
        self.adminprefix = adminprefix
        print('bot initialized.')

    def start(self):
        print('starting bot...')
        super().start()

    def on_welcome(self, serv, event):
        print('got welcome message')
        if self._channels is not None:
            print('joining channels', ', '.join(self._channels))
            for chan in self._channels:
                serv.join(chan)
            print('channels successfully (or not) joined')
        print('listening for triggers started.')

    def on_privmsg(self, serv, event):
        print('PRIVMSG from', event.source.nick)
        cmd, args = unpack(event.arguments[0])
        print('Command {0} with args {1}'.format(cmd, args))
        if cmd in admin.binding.keys():
            print('command exists!')
            ret = admin.binding[cmd](serv, self, event, args)
            if ret is not None:
                for i in ret.split('\n'):
                    serv.notice(event.source.nick, i)

    def on_pubmsg(self, serv, event):
        if event.arguments[0][0] == self.cmdprefix:
            # it is a command
            cmd, args = unpack(event.arguments[0][1:])
            print(event.source.nick, 'launched the', cmd, 'command, with the following arguments:', args)
            if cmd in fantasy.binding.keys():
                print('command exists!')
                # calling the function
                ret = fantasy.binding[cmd](serv, self, event, args)
                if ret is not None:
                    for i in ret.split('\n'):
                        serv.privmsg(event.target, i)

        if event.arguments[0][0] == self.adminprefix:
            # it is an admin command
            cmd, args = unpack(event.arguments[0][1:])
            print(event.source.nick, 'launched the', cmd, 'admin command, with the following arguments:', args)
            if cmd in admin.binding.keys():
                print('command exists!')
                # calling the function
                ret = admin.binding[cmd](serv, self, event, args)
                if ret is not None:
                    for i in ret.split('\n'):
                        serv.privmsg(event.target, i)

    def get_version(self):
        return self.version

    def on_ctcp(self, c, e):
        nick = e.source.nick
        print('got a CTCP', e.arguments[0], 'from', nick)
        if e.arguments[0] == "VERSION":
            c.ctcp_reply(nick, "VERSION " + self.get_version())
        elif e.arguments[0] == "PING":
            if len(e.arguments) > 1:
                c.ctcp_reply(nick, "PING " + e.arguments[1])
