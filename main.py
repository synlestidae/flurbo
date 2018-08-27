from command_op import CommandOp
from create_dir_op import CreateDirOp
from config_file_op import ConfigFileOp
from postfix_conf import PostfixConf
from cert_op import CertOp

email_addrs = {
    "mate@antunovic.nz": "mate"
}

domain = 'antunovic.nz'
hostname = 'mail.antunovic.nz'

cert_op = CertOp(hostname),

commands = [
    cert_op,
    cmd('apt-get install postfix'),
    ConfigFileOp('/etc/postfix/main.cf', PostfixConf, 
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
    ),
    ConfigFileOp('/etc/postfix/virtual', SpaceConf, **email_addrs),
    cmd('systemctl restart postfix'),
    cmd('ufw allow Postfix'),
    LetsEncrypt(domain)
]

def cmd(cmd):
    return CommandOpcmd.split(re.compile('\s+'))

