FROM python:3.8-buster

RUN apt-get update
ADD . /mqtt
WORKDIR /mqtt

RUN pip install -r requirements-mqtt.txt

EXPOSE 5000