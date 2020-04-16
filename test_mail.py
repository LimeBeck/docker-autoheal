import argparse
from email.message import EmailMessage

import config
from send_mail import get_mail_server

parser = argparse.ArgumentParser(description='Send test email')
parser.add_argument('email', type=str,
                    help='Recipient Email')

args = parser.parse_args()

server = get_mail_server()

msg = EmailMessage()
msg.set_content("This is test message")
msg['Subject'] = f"This is test message"
msg['From'] = config.email_from
msg['To'] = args.email

server.send_message(msg)
