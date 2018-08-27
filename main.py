import re
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('domain', help='Need the email domain e.g. for john@example.com it would be example.com')
parser.add_argument('dest', help='Destination to which this server routes email')
parser.add_argument('host', help='Hostname of the server you are setting up')

args = parser.parse_args()

from command_op import CommandOp
from create_dir_op import CreateDirOp
from config_file_op import ConfigFileOp
from postfix_conf import PostfixConf, relay_config
from cert_op import CertOp
from space_conf import SpaceConf

print(args)

domain = args.domain
host = args.host
dest = args.dest

def cmd(cmd):
    cmd = re.split('\s+', cmd)
    return CommandOp(cmd[0], cmd[1:])

cert_op = CertOp(host)
config_postfix = relay_config(host, domain, dest, cert_op)

commands = [
    cmd('add-apt-repository ppa:certbot/certbot'),
    cmd('apt-get update'),
    cmd('apt-get install certbot'),
    cert_op,
    cmd('apt-get install postfix'),
    config_postfix,
    #ConfigFileOp('/etc/postfix/virtual', SpaceConf, **email_addrs),
    cmd('systemctl restart postfix'),
    cmd('ufw allow Postfix'),
]

def main():
    step = 1
    for c in commands:
        print("Step (%d) %s" % (step, c.step_name()))
        if not c.check_ready():
            print(("Cannot run step '%s'. It is not ready or some prerequesite is not satisfied" % c.step_name()))
        try:
            c.run()
        except Exception as e:
            print(e)
            show_step_err(c)
            return 

        if not c.was_success():
            show_step_err(c)
            return
        step += 1

def show_step_err(c):
    print(("Step '%s' failed. Cannot continue, sorry" % c.step_name()))

if __name__ == '__main__':
    main()

