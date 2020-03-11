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

```app1```

`app.py` helps us to expose the REST API in the form of `/get/prediction/v1.0/imageid` and `/get/prediction/v1.0/imageid/<imageid>`.
These two endpoints fetches the data from the mongodb. The first endpoint fetches all the data while the second one allows to selectively fetch the data based on image id.

One can use the rest api to view all classification result by typing the following on the browser:
```
http://localhost:5000/get/prediction/v1.0/imageid/
```
or
```
http://localhost:5000/get/prediction/v1.0/imageid/31231231231
```
for results per image id where `31231231231` is an example of image id.


# ```app2```

`mqtt_client.py` brings about the implementation of mqtt client using python. This client acts as a `subscriber` which subscribes to a topic `new_prediction`. We make use of mosquitto_pub cli to publish messages to the broker using the same topic. Once a message is received at the client, we first validate if the message follows a schema/pattern. This is achived by specifying the pattern in the ``schemaValidator.json``.
Once the message is validated, it is inserted into a mongo databse and is now ready to consumed by the rest api.

```docker-mosquitto``` is the server implementation of MQTT broker.

All the three have individual Dockerfiles which enables them to run on a container.

## Uisng mosquitto_pub for publishing messages

1. First we need to install mosquitto_pub and mosquitto_sub cli tool, freely avavilable on the internet.
2. Next navigate to the folder where mosquitto was installed.
3. Use the below syntax to transmit a message - 
```
mosquitto_pub -t new_prediction -m <JSON>
```
example
```
mosquitto_pub -h localhost -u some_user -P some_pass -p 1883 -d -t new_prediction -m "{\"status\":\"complete\",\"imagePath\":\"20180907\\1536311270718.jpg\",\"imageId\":\"1536311270718\",\"output\":[{\"bbox\":[1008.8831787109375,280.6226501464844,1110.0245361328125,380.72021484375],\"probability\":0.9725130796432495,\"label\":\"nail\",\"result\":\"good\"}]}"
```

The above example follows the schema as outlined in the schemaValidator.json. 


# tearing down of the container

```docker-compose down```
