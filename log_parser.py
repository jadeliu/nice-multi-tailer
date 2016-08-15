#!/usr/bin/python
# -*- coding: <utf-8> -*-

import datetime
import simplejson as json

class LogParser:

    def parse(self, s, filepath):
        try:
            data = json.loads(s)
            data['filepath'] = filepath
        except ValueError:
            data['line'] = s
            print 'error decoding JSON'
            pass
        if 'at' not in data:
            print 'no at key in json'
            data['at'] = datetime.datetime.now()
        self.parse_at_time(data)
        return data

    # function to parse at time in data
    def parse_at_time(self, data_dic):
        if not data_dic:
            print 'no input'
            return
        try:
            data_dic['at'] = datetime.datetime.strptime(data_dic['at'], '%a %b %d %H:%M:%S %Z %Y')
        except ValueError:
            print 'error in parsing at time'
            pass




