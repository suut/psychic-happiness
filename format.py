#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import enum


controlcodes = {'bold':        '\x02',
                'underlined':  '\x1F',
                'italic':      '\x1D',
                'reset':       '\x0F',
                'reverse':     '\x16'}



colorlist = {'white':       '\x0300',
             'black':       '\x0301',
             'blue':        '\x0302',
             'green':       '\x0303',
             'red':         '\x0304',
             'brown':       '\x0305',
             'purple':      '\x0306',
             'orange':      '\x0307',
             'yellow':      '\x0308',
             'lightgreen':  '\x0309',
             'bluegreen ':  '\x0310',
             'cyan':        '\x0311',
             'lightblue':   '\x0312',
             'magenta':     '\x0313',
             'darkgrey':    '\x0314',
             'grey':        '\x0315'}

class Color:
    """use it like that: color.red.blue.bold"""
    def __init__(self):
        self.values = []

    def __getattr__(self, x):
        # the magic function!
        new = type(self)()
        new.values = self.values[:] #make sure to copy the list and not to pass a reference of it
        new.values.append(str(x))
        return new

    def __str__(self):
        bg_color = ''
        fg_color = ''
        c_codes = []
        for i in self.values:
            if i in colorlist.keys():
                if fg_color == '':
                    fg_color = colorlist[i]
                elif bg_color == '':
                    bg_color = colorlist[i]
                else:
                    raise AttributeError('you can\'t specify more than 2 colors')
            elif i in controlcodes.keys():
                c_codes.append(controlcodes[i])
        return fg_color+bg_color+''.join(c_codes)

    def __repr__(self):
        return self.__str__()

color = Color()
