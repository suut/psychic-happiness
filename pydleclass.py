#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

import pydle

class EpikNetExtension(pydle.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def on_raw_335(self, params):
        """the raw numeric 335 tells us that the target user is a bot on the network"""
        source, target, message = params._kw['params']
        self._whois_info[target]['bot'] = True

    def cycle(self):
        """extended cycle function: if no arguments, cycle all channels"""
        if channel is not None:
            parsing.NormalizingDict(self.users, case_mapping=self._case_mapping)
            super().cycle(channel)
        else:
            for channel, password in zip(self.channels.keys(), self.channels.values()):
                self.join(channel, password)

    def complete_host(self, nick):
        if nick not in self.users.keys():
            raise pydle.NotInChannel('went through every channels, user can\'t be found')
        user = self.users[nick]
        return '{}!{}@{}'.format(user['nickname'], user['username'], user['hostname'])
