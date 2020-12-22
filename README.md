# Docker Autoheal
Simple docker autoheal with email notifications

In additional to restart unhealthy containers, 
it allow you to receive email notifications about  

## Install

Available on dockerhub:  `limebeck/docker-autoheal`

Don't forget to add volume with docker socket. 
Usually like this: `-v /var/run/docker.sock:/var/run/docker.sock`

Add to your containers labels:

- Autoheal label (default - autoheal, but you can provide own)
- `failure_notify=true/false` - enable/disable notifications on container
- `failure_notify_email=your@mail.com` - specify email for container
- `failure_notify_timeout=n` - period between notifications, minutes
- `failure_cmd=/command.sh` - any command, run in container just before restart


## Test email

You can send test email with command `docker exec <container_name> python ./test_mail.py your@mail.com`

## Configuration via environment variables
* DEFAULT_SEND_TIMEOUT_MIN - default send timeout for every container, minutes (default - 15)
* DEFAULT_RECEIVER_ADDRESS - default notification receiver email
* EMAIL_FROM - sender email
* EMAIL_HOST - smtp server host
* EMAIL_PORT - smtp server port (default - 465)
* EMAIL_LOGIN - smtp server login (not required)
* EMAIL_PASSWORD - smtp server password (not required)
* EMAIL_ENABLE_TLS - smtp server required tls (default - false)
* EMAIL_USE_SSL - smtp server required ssl (default - false)
* AUTOHEAL_CONTAINER_LABEL - label for containers to watch (default - `autoheal`)
* AUTOHEAL_DEFAULT_STOP_TIMEOUT - docker timeout parameter, seconds (default - 10)
* AUTOHEAL_INTERVAL - check interval, seconds (default - 5)
* AUTOHEAL_START_PERIOD - wait before start, seconds (default - 0)
* AUTOHEAL_DEBOUNCE_TIME - debounce time (default - 0)
* CLEAN_PERIOD - system property. Clean old email message log, minutes (default - 1440, one day)
* DOCKER_BASE_URL - Docker base url (default - unix://var/run/docker.sock)
* DOCKER_CONNECTION_TIMEOUT - Docker connection timeout in seconds (default - 60)

## Build

Clone repository and run `docker build -t limebeck/docker-autoheal:latest -f Dockerfile .`

## Test

Run test container and docker-autoheal service:
1. go to test folder 
2. copy `.env.example` to `.env` and change to your values
3. run `docker-compose up`