FROM python:3.8.2-alpine

COPY ./ .

HEALTHCHECK --start-period=10s --timeout=30s --interval=2s --retries=1 CMD [ "python3", "healthcheck.py" ]

CMD [ "python3", "-u", "app.py" ]