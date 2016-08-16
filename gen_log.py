from random import randrange, randint
from datetime import timedelta, datetime

class LogGenerator:
    def random_date(self):
        start = datetime.strptime('1/1/2015 1:30 PM', '%m/%d/%Y %I:%M %p')
        delta = datetime.now() - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)

    def gen_valid_log(self):
        ti = self.random_date()

        data = {'content':{}, 'note':'note content'}
        ti_str = datetime.strftime(ti, '%a %b %d %H:%M:%S %Y')

        data['at'] = ti_str[:-4] + "PDT "+ti_str[-4:]
        for i in range(randint(1, 5)):
            key = "key"+str(i)
            value = "value"+str(i)
            if randint(0,1):
                key1 = key + '.1'
                value1 = value + '.1'
                value = {key1:value1}
            data['content'].update({key:value})
        return data

    def gen_invalid_log(self):

        with open('./sample_logs/invalid_templates') as f:
            lines = f.readlines()
            line = lines[randint(0, len(lines)-1)]

            # find and replace the content after "at"
            if "at" in line:
                idx = line.find('"at"')
                idx = idx + 4
                start = 0
                while line[idx]!='"':
                    idx +=1
                start = idx
                idx += 1
                while line[idx]!='"':
                    idx += 1
                end = idx
                ti = self.random_date()
                ti_str = datetime.strftime(ti, '%a %b %d %H:%M:%S %Y')
                ti_str = ti_str[:-4] + "PDT "+ti_str[-4:]
                return line[:start]+ti_str+line[end:]
            return line

l = LogGenerator()
print l.gen_invalid_log()
print l.gen_valid_log()