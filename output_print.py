import log_parser
import simplejson as json
import sys
import datetime

class OutputPrinter:
    @classmethod
    def print_valid_line(cls, data_dic):
        data_dic['at'] = datetime.datetime.strftime(data_dic['at'], '%a %b %d %H:%M:%S %Z %Y')
        sys.stdout.write(json.dumps(data_dic, sort_keys=True, indent=4, separators=(',', ': ')))

    @classmethod
    def print_invalid_line(cls, data):
        sys.stderr.write(data['line'])

    def is_valid(self, data_dic):
        if data_dic:
            if ("content" in data_dic) and ("at" in data_dic) and ("note" in data_dic):
                return True
            return False
        return False
