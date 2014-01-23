# -*- coding: utf-8 -*-

import irc.bot

class Enum:
    def __init__(self, *args, **kwargs):
        """ either you can call it like that: Enum(a=1, b=2) #1
            or like that: Enum({'a': 1, 'b': 2}) #2
        """
        if len(args) == 1:  #2
            if type(args[0])==dict and len(kwargs)==0:
                self.internal_dict = args[0]
            else:
                raise ValueError('uncorrect')
        elif len(kwargs)>0: #1
            if len(args)==0:
                self.internal_dict = kwargs
            else:
                raise ValueError('uncorrect')
    def __getattr__(self, name):
        return self.internal_dict.__getitem__(name)

class ServerSpec(irc.bot.ServerSpec):
    def __init__(self, host, nickname, realname, port, password):
        super().__init__(host, port, password)
        self.nickname = nickname
        self.realname = realname

def unpack(raw):
    unpacked = raw.split(sep=' ')
    cmd = unpacked[0].lower()
    args = None
    if len(unpacked) > 1:
        args = unpacked[1:]
    return (cmd, args)
