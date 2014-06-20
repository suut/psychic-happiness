#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

#here's we're testing some things to prepare the migration to the pydle irc library

import pydle


class SuperBot(pydle.Client):
    def on_connect(self):
        self.join('#pigeons')

    @pydle.coroutine
    def on_channel_message(self, target, source, message):
        print(source, '=>', target, ':', message)
        info = yield self.whois(source)
        for key, val in zip(info.keys(), info.values()):
            print(key, '=>', val)



client = SuperBot('suutbot', realname='suut\'s bot')
client.connect('irc.epiknet.org', 7002, tls=True, tls_verify=False)
client.handle_forever()
