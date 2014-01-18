# -*- coding: utf-8 -*-

import IRCBot, configparser, util

# let's parse the config options

confparser = configparser.ConfigParser()
servparser = configparser.ConfigParser()

confparser.read('config.ini')
servparser.read('servers.ini')

chosen_server = confparser['connect']['server']

# let's verify if the server is defined in the servers.ini file

assert chosen_server in servparser.sections(), 'server does not exist'

serv_details = servparser[chosen_server]

password = None
channels = None

if serv_details['password'] != '':
    password = serv_details['password']

if serv_details['channels'] != '':
    channels = serv_details['channels'].split(',')

server = util.ServerSpec(serv_details['host'], serv_details['nickname'], serv_details['realname'], int(serv_details['port']), password)

bot = IRCBot.SpiderBot(server, channels, confparser['misc']['version'], confparser['bot']['cmdprefix'], confparser['bot']['adminprefix'])

bot.connection.buffer_class.encoding = serv_details['charset']

bot.start()
