FROM python:3.8.2-alpine

LABEL maintainer="becklime@gmail.com"

WORKDIR /app

HEALTHCHECK --start-period=10s --timeout=30s --interval=60s --retries=3 CMD [ "python3", "healthcheck.py" ]

COPY ./requirements.txt /

RUN pip install -r /requirements.txt

COPY ./src /app

CMD [ "python3", "-u", "app.py" ]