import os
from typing import Optional
from dotenv import load_dotenv

from utils import get_required_env, to_bool, log

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

default_send_timeout_min: int = int(os.getenv("DEFAULT_SEND_TIMEOUT_MIN", 15))
default_receiver_address: str = get_required_env("DEFAULT_RECEIVER_ADDRESS")
email_from: str = get_required_env("EMAIL_FROM")
email_host: str = get_required_env("EMAIL_HOST")
email_port: int = int(os.getenv("EMAIL_PORT", 465))
email_login: Optional[str] = os.getenv("EMAIL_LOGIN")
email_password: Optional[str] = os.getenv("EMAIL_PASSWORD")
email_enable_tls: bool = to_bool(os.getenv("EMAIL_ENABLE_TLS", False))
email_use_ssl: bool = to_bool(os.getenv("EMAIL_USE_SSL", False))
container_label: str = os.getenv("AUTOHEAL_CONTAINER_LABEL", "autoheal")
container_stop_timeout: int = int(os.getenv("AUTOHEAL_DEFAULT_STOP_TIMEOUT", 10))
container_interval: int = int(os.getenv("AUTOHEAL_INTERVAL", 5))
container_start_period: int = int(os.getenv("AUTOHEAL_START_PERIOD", 0))
container_debounce_time: int = int(os.getenv("AUTOHEAL_DEBOUNCE_TIME", 0))
clean_period: int = int(os.getenv("CLEAN_PERIOD", 24 * 60))
docker_base_url: str = os.getenv("DOCKER_BASE_URL", "unix://var/run/docker.sock")
docker_timeout: int = int(os.getenv("DOCKER_CONNECTION_TIMEOUT", 60))


log(f"""Configuration:
DEFAULT_SEND_TIMEOUT_MIN={default_send_timeout_min}
DEFAULT_RECEIVER_ADDRESS={default_receiver_address}
EMAIL_FROM={email_from}
EMAIL_HOST={email_host}
EMAIL_PORT={email_port}
EMAIL_LOGIN={email_login}
EMAIL_PASSWORD={email_password}
EMAIL_ENABLE_TLS={email_enable_tls}
EMAIL_USE_SSL={email_use_ssl}
AUTOHEAL_CONTAINER_LABEL={container_label}
AUTOHEAL_DEFAULT_STOP_TIMEOUT={container_stop_timeout}
AUTOHEAL_INTERVAL={container_interval}
AUTOHEAL_START_PERIOD={container_start_period}
AUTOHEAL_DEBOUNCE_TIME={container_debounce_time}
CLEAN_PERIOD={clean_period}
DOCKER_BASE_URL={docker_base_url}
""".rstrip()
)
