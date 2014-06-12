#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

# IRC bot
# Roadmap:
#   [X] Functions core
#   [X] Bot backbone
#   [X] Server loader
#   [ ] Per-server config loader
#   [ ] Functions registry
#   [ ] Highest priority functions (auth)
# /!\ NO GLOBAL CONF, ONLY PER-SERVER CONF /!\
# when config changes, (1) apply it OTF,
#              (2) save it immediately to disk

#TODO: saveconfig(), rehash()

import functions, admin, reload #for the code to be executed
from core import chosen_server
from superbot import SuperBot

bot = SuperBot(chosen_server)

bot.start()
