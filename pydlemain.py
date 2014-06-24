#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

#here's we're testing some things to prepare the migration to the pydle irc library

from pydleclass import EpikNetExtension
from pydle import coroutine
from functions_core import _process_cmd


class SuperBot(EpikNetExtension):
    def on_connect(self):
        self.join('#kitchen')

    @coroutine
    def on_channel_message(self, target, source, message):
        #def process_cmd(msg, source, target, serv, channels, callback):
        _process_cmd(message, target, source, self)
        #info = yield self.whois(source)

#def f_wrapper(args, source, target, bot)

#args = (1, 2)
#source =

client = SuperBot('suutbot', realname='suut\'s bot')
client.connect('irc.epiknet.org', 7002, tls=True, tls_verify=False)
print('connecting')
client.handle_forever()
