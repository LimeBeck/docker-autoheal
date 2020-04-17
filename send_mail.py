import smtplib
import config


def get_mail_server():
    if bool(config.email_use_ssl):
        email_server = smtplib.SMTP_SSL(config.email_host, config.email_port)
    else:
        email_server = smtplib.SMTP(config.email_host, config.email_port)

    if config.email_login:
        email_server.login(config.email_login, config.email_password)
    return email_server
