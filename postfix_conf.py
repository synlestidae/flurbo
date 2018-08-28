import os
import re

from config_file_op import ConfigFileOp

class PostfixConf: 
    def __init__(self, path, **vals):
        self.path = path
        self.vals = []
        for k in vals:
            self.append_kv(k, vals[k])

    def __enter__(self):
        print("Have %d lines to write to file" % len(self.vals));
        self.lines = []

        if not os.path.exists(self.path):
            return self

        with open(self.path, 'r') as f:
            for row in f:
                self.vals.append(self.parse_row(row))

        print("Now have to write %d lines" % len(self.vals))
        return self

    def __exit__(self, ty, value, traceback):
        print("Writing %d rows to %s" % (len(self.vals), self.path))
        lines = []
        f = open(self.path, 'w')
        for row in self.vals:
            row_str = str(row).strip()
            if row is not None and row.key is not None:
                f.write(row_str + "\n")
            elif row is None:
                f.write("\n")
        f.close()

    def __getitem__(self, pos):
        for row in self.vals:
            if row.key is not None and row.key == pos:
                return row.value

    def __setitem__(self, key, value):
        for row in self.vals:
            if row.key is not None and row.key == key:
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
            comment = None
            k, v = text.split('=', 1)
            return ConfigParam(k.strip(), v.strip())
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

def relay_config(host, domain, dst_host, cert_op):
    return ConfigFileOp('/etc/postfix/main.cf', PostfixConf, 
        inet_interfaces = 'loopback-only',
        myorigin = host, 
        mydomain = domain,
        myhostname = host,
        mydestination = '',
        relayhost = dst_host,
        local_transport='error= local delivery disabled',
        # Still need ssh shit to work
        smtpd_use_tls= 'yes',
        smtpd_tls_cert_file = cert_op.cert_path,
        smtpd_tls_key_file = cert_op.key_path,
        smtpd_tls_security_level = 'encrypt',
        smtpd_tls_auth_only='yes',
        smtpd_recipient_restrictions = 'permit_sasl_authenticated,reject_invalid_hostname,reject_unknown_recipient_domain,reject_unauth_destination,reject_rbl_client sbl.spamhaus.org,permit'
    )

def normal_config(host, domain, username):
    return ConfigFileOp('/etc/postfix/main.cf', PostfixConf, 
        myhostname = host,
        mydomain = domain,
        myorigin = host, 
        mydestination = domain,
        home_mailbox="Maildir/", 
        virtual_alias_maps= 'hash:/etc/postfix/virtual',
        smtpd_use_tls= 'yes',
        smtpd_tls_cert_file = cert_op.cert_path,
        smtpd_tls_key_file = cert_op.key_path,
        smtpd_tls_security_level = 'encrypt',
        smtpd_tls_auth_only='yes',
        smtpd_recipient_restrictions = '''permit_sasl_authenticated,
            reject_invalid_hostname,
            reject_unknown_recipient_domain,
            reject_unauth_destination,
            reject_rbl_client sbl.spamhaus.org,
            permit'''
    )
