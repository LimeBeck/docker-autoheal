from time import sleep
from datetime import datetime, timezone
import smtplib
from email.message import EmailMessage
from collections import namedtuple
from typing import List

from docker import DockerClient

import dateutil.parser as parser
from docker.models.containers import Container

from send_mail import get_mail_server
from utils import log, LogLevel
import config

SendedEmail = namedtuple("SendedEmail", ["send_time", "container_name", "email", "message", "result", "response"])
Email = namedtuple("Email", ["address", "container_name", "failure_time", "healthcheck_response"])
unhealth_containers: List[Container] = []
sended_emails: List[SendedEmail] = []

log(f"""Start with configuration:
DEFAULT_SEND_TIMEOUT_MIN={config.default_send_timeout_min}
DEFAULT_RECEIVER_ADDRESS={config.default_receiver_address}
EMAIL_FROM={config.email_from}
EMAIL_HOST={config.email_host}
EMAIL_PORT={config.email_port}
EMAIL_LOGIN={config.email_login}
EMAIL_PASSWORD={config.email_password}
EMAIL_ENABLE_TLS={config.email_enable_tls}
EMAIL_USE_SSL={config.email_use_ssl}
AUTOHEAL_CONTAINER_LABEL={config.container_label}
AUTOHEAL_DEFAULT_STOP_TIMEOUT={config.container_stop_timeout}
AUTOHEAL_INTERVAL={config.container_interval}
AUTOHEAL_START_PERIOD={config.container_start_period}
AUTOHEAL_DEBOUNCE_TIME={config.container_debounce_time}
CLEAN_PERIOD={config.clean_period}
DOCKER_BASE_URL={config.docker_base_url}
""".rstrip()
    )

docker_client = DockerClient(base_url=config.docker_base_url)
docker_client.ping()

email_server = get_mail_server()


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
    except smtplib.SMTPServerDisconnected:
        email_server.connect()


def notify_failure(container: Container, time: datetime):
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
    if "failure_notify_timeout" in container.labels.keys():
        send_timeout = int(container.labels['failure_notify_timeout'])
    if not latest_send or (time - latest_send.send_time).seconds / 60 > send_timeout:
        default_address = config.default_receiver_address
        addresses = [default_address]
        if 'failure_notify_email' in container.labels.keys():
            addresses = container.labels['failure_notify_email'].split(',')
        for address in addresses:
            send_email(Email(
                address=address,
                container_name=container.name,
                failure_time=failure_time,
                healthcheck_response=healthcheck_response
            ))


def restart_container(container: Container):
    log(f"<27db178e> Restaring container {container.name} with timeout {config.container_stop_timeout}")
    container.restart(timeout=config.container_stop_timeout)


def process_container(container: Container):
    log(f"<193643d5> Container {container.name} seems to be unhealthy")
    now = datetime.now(timezone.utc)
    failure_time = container.attrs["State"]["Health"]["Log"][-1]["End"]
    try:
        parsed_time = parser.isoparse(failure_time)
        if (now - parsed_time).seconds > config.container_debounce_time:
            restart_container(container)
            if container.labels.get("failure_notify"):
                notify_failure(container, now)
    except Exception as e:
        log(f"<22105c76> Error in container ({container.name}) processing: {e}", LogLevel.ERROR)


def start():
    sleep(config.container_start_period)
    while True:
        sleep(config.container_interval)
        for container in docker_client.containers.list(
                filters={"health": "unhealthy", "label": [f"{config.container_label}=true"]}):
            process_container(container)


if __name__ == "__main__":
    try:
        start()
    finally:
        docker_client.close()
        email_server.quit()
