# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN pip3 install -r requirements.txt

COPY . .

# testing locally CMD [ "python3", "run.py"]
ENTRYPOINT ["./gunicorn.sh"]
