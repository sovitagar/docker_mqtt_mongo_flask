import json
import time
from jsonschema import validate
import paho.mqtt.client as mqtt
from pymongo import MongoClient


def data_validation(schema, json_data):
    # function to validate the subscribed data
    if validate(instance=json_data, schema=validator) is None:
        return 1
    else:
        return 0


mclient = MongoClient("mongodb", 27017)  # connection to mongodb
db = mclient.demo  # demo is the db name
# print("db: ", db)

# reading the schema or json format of the topic
with open("schemaValidator.json") as f:
    validator = json.load(f)

collection = db["mycol"]  # "mycol" is the collection name
# print("col: ", collection)

# creating an mqtt client
client = mqtt.Client()
client.username_pw_set("some_user", "some_pass")  # dummy username and pwd


# on connect to MQTT server to subscribe to our topic "new_prediction"
def on_connect(client, userdata, flags, rc):
    client.subscribe("new_prediction")


def on_message(client, userdata, msg):
    # validate and push data to db on receipt of messgae

    print("Data received")
    print("Topic: " + msg.topic)
    print("Extracting data ")
    try:
        message_json = json.loads(msg.payload)
        try:
            if data_validation(validator, message_json):
                print("inserting into database")
                entry_id = collection.insert_one(message_json).inserted_id
                print("Success. Document id : " + str(entry_id))
            else:
                print("data validation failed")
        except Exception as e:
            print("error :", str(e))
    except Exception as e:
        print("error :", str(e))


client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt", 1883, 120)
client.loop_start()

while True:
    time.sleep(0.05)
