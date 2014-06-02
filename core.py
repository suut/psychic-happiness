#!/usr/bin/python3.3
# -*- coding: utf-8 -*-

# core.py
# Functions:
#   [X] ToSend object
#   [X] loading servers details
#   [X] loading servers config (in which is found username, etc.)
#   [ ] logging to disk commands and status
#   [ ] loading and providing configuration e.g. is_enabled()
#   [ ] provides ini reading interface

import irc.bot, configparser
import sys

class ServerSpec(irc.bot.ServerSpec):
    def __init__(self, host, port, password, nickname, username, realname, channels):
        if password == '':
            password = None
        super().__init__(host, port, password)
        self.nickname = nickname
        self.realname = realname
        self.username = username
        self.channels = channels

class ToSend:
    """ a class to ease the slicing of messages to send """
    def __init__(self, target, content):
        #TODO: split the msg in 512o chunks
        self.target = target
        self.content = content.split('\n')

# LOADING SERVERS CONFIG
#sys.argv.append('quakenet')
#TODO: ^spoofing the cmdline for testing purposes, TO REMOVE
print('booting up...')
_serversparser = configparser.ConfigParser()
_serversparser.read('servers.ini')
print('available servers:', ', '.join(_serversparser.sections()))
assert len(sys.argv) > 1, 'you must provide a server to connect to'
assert sys.argv[1] in _serversparser.sections(), '{0} server does not exist'.format(sys.argv[1])
print('will connect to {0} ({1}:{2})'.format(sys.argv[1],
                         _serversparser[sys.argv[1]]['host'],
                         _serversparser[sys.argv[1]]['port']))

#loading server details
server_config = configparser.ConfigParser()
server_config.read('config/{0}.ini'.format(sys.argv[1]))
_details = server_config['details']

def write_config():
    with open('config/{0}.ini'.format(sys.argv[1]), mode='w') as f:
        server_config.write(f)

#creating the ServerSpec object
chosen_server = ServerSpec(_serversparser[sys.argv[1]]['host'],
               int(_serversparser[sys.argv[1]]['port']),
               _serversparser[sys.argv[1]]['password'],
               _details['nickname'],
               _details['username'],
               _details['realname'],
               _details['channels'].split(','))

format = {'bold': '',
           'underlined': '',
           'reset': ''}

with open('VERSION') as file:
    version = file.read()