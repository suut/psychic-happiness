#!/usr/bin/python3.3
# -*- coding: utf-8 -*-

# core.py
# Functions:
#   [X] loading servers details
#   [X] loading servers config (in which is found username, etc.)
#   [ ] logging to disk commands and status
#   [ ] loading and providing configuration e.g. is_enabled()
#   [ ] provides ini reading interface

import irc.bot, configparser
import sys

class ServerSpec(irc.bot.ServerSpec):
    def __init__(self, host, port, password, nickname, username, realname, channels, modes):
        if password == '':
            password = None
        super().__init__(host, port, password)
        self.nickname = nickname
        self.realname = realname
        self.username = username
        self.channels = channels
        self.modes = modes

# LOADING SERVERS CONFIG
#sys.argv[1] = 'quakenet'
#TODO: ^spoofing the cmdline for testing purposes, TO REMOVE
print('booting up...')
_serversparser = configparser.ConfigParser()
_serversparser.read('config/servers.ini')
print('available servers:', ', '.join(_serversparser.sections()))
assert len(sys.argv) > 1, 'you must provide a server to connect to'
assert sys.argv[1] in _serversparser.sections(), '{0} server does not exist'.format(sys.argv[1])
print('will connect to {0} ({1}:{2})'.format(sys.argv[1],
                         _serversparser[sys.argv[1]]['host'],
                         _serversparser[sys.argv[1]]['port']))

#loading server details
server_config = configparser.ConfigParser()
server_config.read('config/{0}.ini'.format(sys.argv[1]))
details = server_config['details']


def write_config():
    with open('config/{0}.ini'.format(sys.argv[1]), mode='w') as f:
        server_config.write(f)

#creating the ServerSpec object
chosen_server = ServerSpec(_serversparser[sys.argv[1]]['host'],
               int(_serversparser[sys.argv[1]]['port']),
               _serversparser[sys.argv[1]]['password'],
               details['nickname'],
               details['username'],
               details['realname'],
               details['channels'].split(','),
               details['modes'])

format = {'bold': '',
           'underlined': '',
           'reset': ''}

with open('VERSION') as file:
    version = file.read()


def split(txt, target):
    # split according to \n in text
    # split in 512 bytes (and be careful not to split in the middle of a UTF-8 control code)
    final_text = []
    for i in txt.split('\n'):
        if len(i.encode())+len(target.encode()) >= 500:
            # "PRIVMSG #channel :message\r\n" must not exceed 512 bytes
            s = i.encode()
            splitted = []
            cursor = 500-len(target)
            while ''.join(j.decode() for j in splitted) != i:
                try:
                    s[:cursor].decode()
                except UnicodeDecodeError:
                    cursor -= 1
                splitted.append(s[:cursor])
                s = s[cursor:]
                cursor -= len(s)
            final_text += [k.decode() for k in splitted]
        else:
            final_text.append(i)
    return final_text
