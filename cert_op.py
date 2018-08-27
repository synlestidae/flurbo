import subprocess
from command_op import CommandOp

class CertOp:
    def __init__(self, domain, cert_path = "/etc/letsencrypt/live/%s/fullchain.pem", key_path = "/etc/letsencrypt/live/%s/privkey.pem"):
        self.domain = domain
        self.bot_command = CommandOp('certbot', ['certonly', '--standalone', '-d', self.domain])
        self.cert_path = cert_path % domain
        self.key_path = key_path % domain

    def check_ready(self):
        # can bind to port 80
        # certbot command exists
        return True # TODO check that certbot exists 

    def run(self):
        return self.bot_command.run()

    def was_success(self):
        return self.bot_command.was_success()
        pass
