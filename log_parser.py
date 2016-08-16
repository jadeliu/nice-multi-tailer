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
            print s
            print 'error decoding JSON'
            pass
        LogParser.parse_at_time(data)
        if 'at' not in data:
            print 'no at key in json, using current timestamp instead'
            data['at'] = datetime.datetime.now()
        return data

    @staticmethod
    # function to parse at time in data
    def parse_at_time(data_dic):
        if not data_dic:
            print 'no input'
            return
        try:
            if 'at' in data_dic:
                data_dic['at'] = datetime.datetime.strptime(data_dic['at'], '%a %b %d %H:%M:%S %Z %Y')
        except ValueError:
            print 'error in parsing at time'
            pass




