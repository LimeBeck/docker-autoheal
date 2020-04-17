FROM python:3.8.2-alpine

LABEL maintainer="becklime@gmail.com"

COPY ./ /app

WORKDIR /app

RUN pip install -r requirements.txt

HEALTHCHECK --start-period=10s --timeout=30s --interval=2s --retries=1 CMD [ "python3", "healthcheck.py" ]

CMD [ "python3", "app.py" ]