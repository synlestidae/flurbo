import subprocess
from command_op import CommandOp

class CertOp:
    def __init__(self, domain):
        self.domain = domain
        self.bot_command = CommandOp(['certbot', 'certonly', '--standalone', '-d', self.domain])

    def check_ready(self):
        # can bind to port 80
        # certbot command exists
        return True # TODO check that certbot exists 

    def run(self):
        return self.bot_command.run()

    def was_success(self):
        return self.bot_command.was_success()
        pass
