import postfix_conf
import re

class SpaceConf(postfix_conf.PostfixConf):
    def parse_row(self, row):
        items = re.split('\s+', row)
        row = Row()
        row.key = items[0]
        row.items = items[1:]
        return row

    def append_kv(self, key, value):
        r = Row()
        r.key = key
        r.items = [value]
        self.vals.append(r)

class Row:
    def __init__(self):
        self.key = None
        self.items = []

    def __str__(self):
        if self.key is None:
            return ''
        return "%s\t%s\n" % (self.key, ' '.join(self.items))

