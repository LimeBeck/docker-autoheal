import smtplib
from collections import namedtuple
from datetime import datetime, timezone
from email.message import EmailMessage
from typing import List

from docker.models.containers import Container

from labels import FAILURE_NOTIFY_TIMEOUT, FAILURE_NOTIFY_EMAIL, FAILURE_NOTIFY
from utils import log, LogLevel, to_bool

import config


def get_mail_server() -> smtplib.SMTP:
    if bool(config.email_use_ssl):
        email_server = smtplib.SMTP_SSL(config.email_host, config.email_port)
    else:
        email_server = smtplib.SMTP(config.email_host, config.email_port)

    if config.email_login:
        email_server.login(config.email_login, config.email_password)
    return email_server


SendedEmail = namedtuple("SendedEmail", ["send_time", "container_name", "email", "message", "result", "response"])
Email = namedtuple("Email", ["address", "container_name", "failure_time", "healthcheck_response"])
sended_emails: List[SendedEmail] = []


def clean_old_messages():
    now = datetime.now(timezone.utc)
    old_messages = list(
        sorted(filter(lambda x: (x.send_time - now).seconds / 60 > config.clean_period, sended_emails),
               key=lambda x: x.send_time))
    for message in old_messages:
        sended_emails.remove(message)


def send_email(email: Email):
    log(f"<64d4a81f> Send mail {email}")
    msg = EmailMessage()
    msg.set_content(
        f"Container '{email.container_name}' falling down at {email.failure_time} with healthcheck message: \n{email.healthcheck_response}")
    msg['Subject'] = f"Container '{email.container_name}' falling down"
    msg['From'] = config.email_from
    msg['To'] = email.address

    try:
        with get_mail_server() as email_server:
            response = email_server.send_message(msg)
            mail = SendedEmail(
                send_time=datetime.now(timezone.utc),
                container_name=email.container_name,
                email=email,
                message=msg,
                result='SUCCESS',
                response=response
            )
            sended_emails.append(mail)
            log(f"<06b50cf0> Send mail success: {mail}")
    except Exception as e:
        log(f"<e2a98def> ({email.container_name}) Error while send email {email}: {e}", log_level=LogLevel.ERROR)


def notify_failure(container: Container):
    if not to_bool(container.labels.get(FAILURE_NOTIFY)):
        log(
            f"<8133c8b6> ({container.name}) Skip send container failure message because " +
            f"of 'failure_notify'={container.labels.get(FAILURE_NOTIFY)}")
        return
    time = datetime.now(timezone.utc)
    failure_time = container.attrs["State"]["Health"]["Log"][-1]["End"]
    healthcheck_response = container.attrs["State"]["Health"]["Log"][-1]["Output"]
    if type(healthcheck_response) is str:
        healthcheck_response = healthcheck_response.strip()
    latest_send = None
    container_sends = list(
        sorted(filter(lambda x: x.container_name == container.name, sended_emails),
               key=lambda x: x.send_time))
    if len(container_sends) > 0:
        latest_send = container_sends[-1]
    send_timeout = config.default_send_timeout_min
    if FAILURE_NOTIFY_TIMEOUT in container.labels.keys():
        send_timeout = int(container.labels[FAILURE_NOTIFY_TIMEOUT])
    if not latest_send or (time - latest_send.send_time).seconds / 60 > send_timeout:
        default_address = config.default_receiver_address
        addresses = [default_address]
        if FAILURE_NOTIFY_EMAIL in container.labels.keys():
            addresses = container.labels[FAILURE_NOTIFY_EMAIL].split(',')
        log(f"<ad25da5b> ({container.name}) Send container failure message to: {addresses}")
        for address in addresses:
            send_email(Email(
                address=address,
                container_name=container.name,
                failure_time=failure_time,
                healthcheck_response=healthcheck_response
            ))
    else:
        log(
            f"<8133c8b6>  ({container.name}) Skip send container failure message because " +
            f"of send timeout: {send_timeout} minutes")
