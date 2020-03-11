FROM python:3.8-buster
RUN apt-get update
ADD . /flask
WORKDIR /flask

RUN pip install -r requirements.txt

EXPOSE 5000