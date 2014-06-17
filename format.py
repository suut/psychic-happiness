#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import enum


controlcodes = {'bold':        '\x02',
                'underlined':  '\x1F',
                'italic':      '\x1D',
                'reset':       '\x0F',
                'reverse':     '\x16'}



colorlist = {'white':       '00',
             'black':       '01',
             'blue':        '02',
             'green':       '03',
             'red':         '04',
             'brown':       '05',
             'purple':      '06',
             'orange':      '07',
             'yellow':      '08',
             'lightgreen':  '09',
             'bluegreen ':  '10',
             'cyan':        '11',
             'lightblue':   '12',
             'magenta':     '13',
             'darkgrey':    '14',
             'grey':        '15'}

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
                    fg_color = '\x03'+colorlist[i]
                elif bg_color == '':
                    bg_color = ','+colorlist[i]
                else:
                    raise AttributeError('you can\'t specify more than 2 colors')
            elif i in controlcodes.keys():
                c_codes.append(controlcodes[i])
        return fg_color+bg_color+''.join(c_codes)

    def __repr__(self):
        return self.__str__()

color = Color()
