import os
import json
import logging
import psycopg2
from typing import Dict
from kafka import KafkaConsumer

KAFKA_URL = os.environ["KAFKA_URL"]
KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=[KAFKA_URL])


def add_location(location: Dict):
    session = psycopg2.connect(dbname=DB_NAME, port=DB_PORT, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST)
    cursor = session.cursor()
    cursor.execute(
        "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}));".format(
            int(location["person_id"]), float(location["latitude"]), float(location["longitude"])
        )
    )
    session.commit()
    cursor.close()
    session.close()
    print("Location added to the database!")
    return location


def consume_message():
    for message in consumer:
        location = json.loads(message.value.decode("utf-8"))
        add_location(location)


logging.basicConfig(level=logging.WARNING)
consume_message()
