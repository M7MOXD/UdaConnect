import os
import time
import json
import grpc
import logging
import location_pb2
import location_pb2_grpc
from kafka import KafkaProducer
from concurrent import futures

KAFKA_URL = os.environ["KAFKA_URL"]
KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]

# producer = KafkaProducer(bootstrap_servers=["my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092"])
producer = KafkaProducer(bootstrap_servers=KAFKA_URL)


class LocationService(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        print("received")
        location = {"person_id": request.person_id, "latitude": request.latitude, "longitude": request.longitude}
        producer.send(KAFKA_TOPIC, json.dump(location))
        producer.flush()
        return location_pb2.LocationMessage(**location)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationService(), server)

logging.basicConfig(level=logging.WARNING)
print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
