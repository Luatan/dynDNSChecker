FROM python:3.10-alpine

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./src/ .

RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "$(pwd)" \
    --no-create-home \
    checker && \
    chown checker /app

USER checker

ENTRYPOINT ["python3", "./main.py"]

