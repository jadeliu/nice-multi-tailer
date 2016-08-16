from random import randrange, randint, choice
from datetime import timedelta, datetime
import os, time

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
        for i in range(1, randint(1, 5)):
            key = "key"+str(i)
            value = "value"+str(i)
            if randint(0,1):
                key1 = key + '.1'
                value1 = value + '.1'
                value = {key1:value1}
            data['content'].update({key:value})
        return data

    def gen_invalid_log(self):

        with open('./invalid_templates') as f:
            lines = f.readlines()
            line = lines[randint(0, len(lines)-1)]

            # find and replace the content after "at"
            if "at" in line:
                idx = line.find('"at"')
                idx = idx + 4
                start = idx
                while line[idx]!='"':
                    idx +=1
                idx += 1
                start = idx
                while line[idx]!='"':
                    idx += 1
                end = idx
                ti = self.random_date()
                ti_str = datetime.strftime(ti, '%a %b %d %H:%M:%S %Y')
                ti_str = ti_str[:-4] + "PDT "+ti_str[-4:]
                return line[:start]+ti_str+line[end:]
            return line

def write_to_file(filename, line):
    with open(filename, 'a') as f:
        print line
        f.write(str(line)+ os.linesep)
        f.flush()
        f.close()

if __name__=="__main__":
    l = LogGenerator()
    while True:
        file_paths = ['sample_logs/' + k for k in os.listdir('sample_logs')]
        l1 = l.gen_invalid_log()
        write_to_file(choice(file_paths), l1)
        l2 = l.gen_valid_log()
        write_to_file(choice(file_paths), l2)
        l3 = l.gen_valid_log()
        write_to_file(choice(file_paths), l3)
        #time.sleep(10)
