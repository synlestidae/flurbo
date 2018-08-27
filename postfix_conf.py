import os
import re

class PostfixConf: 
    def __init__(self, path, **vals):
        self.path = path
        self.vals = []
        for k in vals:
            self.vals.append(self.append_kv(k, vals[k]))

    def __enter__(self):
        self.lines = []

        if not os.path.exists(self.path):
            return self

        with open(self.path, 'r') as f:
            for row in f:
                self.vals.append(self.parse_row(row))

        return self

    def __exit__(self, ty, value, traceback):
        with open(self.path, 'w') as f:
            for row in self.vals:
                if row is not None and row.key is not None:
                    f.write(str(row))

    def __getitem__(self, pos):
        for row in self.vals:
            if row.key is not None and row.key == pos:
                return row.value

    def __setitem__(self, key, value):
        for row in self.vals:
            if row.key is not None and row.key == pos:
                row.value = value
                return

        self.append_kv(key, value)

    def append_kv(self, key, value):
        self.vals.append(ConfigParam(key, value))

    def parse_row(self, row):
        for p in [Comment, ConfigParam, RawLine]:
            result = p.parse(row);
            if result:
                return result

class Comment:
    def __init__(self, comment):
        self.key = None
        self.comment = comment.rstrip()

    @staticmethod
    def parse(text):
        if re.compile('\s*#').match(text):
            return Comment(text)

    def __str__(self):
        if len(self.comment):
            return "#%s" % self.comment if self.comment[0] != '#' else self.comment
        return ''

class ConfigParam:
    def __init__(self, key, value, comment=None):
        self.key = key
        self.value = value
        self.comment = comment

    @staticmethod
    def parse(text):
        try:
            kv_text, comment = text.split('#', 1)
            regex = re.compile('([A-Za-z_][A-Za-z0-9]*)\s*=\s*(\S*)')
            match = regex.match(kv_text)
            if match:
                key, value = match.groups()
                return ConfigParam(key, value.trim())
        except ValueError:
            return None

    def __str__(self):
        return "%s = %s%s" % (self.key, self.value, str(self.comment).trim() if self.comment is not None else '')

class RawLine:
    def __init__(self, line):
        self.key = None
        self.line = line

    @staticmethod
    def parse(text):
        return RawLine(text)

    def __str__(self):
        return self.line
