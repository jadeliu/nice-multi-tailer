import datetime
import simplejson as json

class LogParser:
    @staticmethod
    def parse(s, filepath):
        data = {}
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
        LogParser.parse_at_time(data)
        return data

    @staticmethod
    # function to parse at time in data
    def parse_at_time(data_dic):
        if not data_dic:
            print 'no input'
            return
        try:
            data_dic['at'] = datetime.datetime.strptime(data_dic['at'], '%a %b %d %H:%M:%S %Z %Y')
        except ValueError:
            print 'error in parsing at time'
            pass




