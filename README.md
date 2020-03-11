# docker_mqtt_mongo_flask
dockerized mqtt server application with mongodb and rest api via flask

The aim of this work is to write a service that stores results from a classification service in a database and make them available through a REST API. The classification service is supported by pub-sub mechanism of MQTT. Here we use MQTT based bus called Mosquitto.

The code is structured in three levels.
``app1`` - which renders the REST API using flask 
``app2`` - which implements the MQTT client using python
``docker-mosquitto`` - which is used to instantiate the MQTT broker/server.


All the three are very cleanly implemented using docker and runs in its own container. And is ``mongodb`` which is also run on a container.

``docker-compose.yaml`` file sets up the individual docker contaiers while also harbouring communication between individual containers.

# Setup

1. Clone the repository.
2. One needs to install `docker` and `docker-compose` in order to run this implementation.
3. All the other dependencies are managed by the individual Dockerfiles.
4. Navidate to the main folder.
# Run

Using command prompt,

1. docker build using ``` docker-compose build```
2. docker run using ```docker-compose up```

After all the containers are up and running, on the command prompt we can see the details of individual containers running and printing messages.

# Understanding of the code

```APP1```

# tearing down of the container

```docker-compose down```
