import os
from dotenv import load_dotenv

from utils import get_required_env, to_bool

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

default_send_timeout_min = int(os.getenv("DEFAULT_SEND_TIMEOUT_MIN", 15))
default_receiver_address = get_required_env("DEFAULT_RECEIVER_ADDRESS")
email_from = get_required_env("EMAIL_FROM")
email_host = get_required_env("EMAIL_HOST")
email_port = int(os.getenv("EMAIL_PORT", 465))
email_login = os.getenv("EMAIL_LOGIN")
email_password = os.getenv("EMAIL_PASSWORD")
email_enable_tls = to_bool(os.getenv("EMAIL_ENABLE_TLS", False))
email_use_ssl = to_bool(os.getenv("EMAIL_USE_SSL", False))
container_label = os.getenv("AUTOHEAL_CONTAINER_LABEL", "autoheal")
container_stop_timeout = int(os.getenv("AUTOHEAL_DEFAULT_STOP_TIMEOUT", 10))
container_interval = int(os.getenv("AUTOHEAL_INTERVAL", 5))
container_start_period = int(os.getenv("AUTOHEAL_START_PERIOD", 0))
container_debounce_time = int(os.getenv("AUTOHEAL_DEBOUNCE_TIME", 0))
clean_period = int(os.getenv("CLEAN_PERIOD", 24 * 60))
docker_base_url = os.getenv("DOCKER_BASE_URL", "unix://var/run/docker.sock")
