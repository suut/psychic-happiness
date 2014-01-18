# -*- coding: utf-8 -*-

import hashlib, configparser
from util import Enum

"""
admnin protocol:
    def ...(source, args):
        ...
        return value_that_will_be_printed_to_channel
"""

encode_passwd = lambda s: hashlib.sha1(s.encode('UTF-8')).hexdigest()

users = configparser.ConfigParser()
users.read('users.ini')

privileges = Enum({'known': 1<<0,
                   'master': 1<<1,
                   'admin': 1<<2})

logged_in = []

def whoami(source, args):
    """tells you what level of privileges do you have"""
    if source.nick in users.sections():
        return 'Privilege level: {0}'.format(users[source.nick]['privileges'])
    else:
        return 'You\'re nobody, lil boy.'

##############################
# NO DEFINE BELOW THIS POINT #
##############################

binding = {'whoami': whoami}