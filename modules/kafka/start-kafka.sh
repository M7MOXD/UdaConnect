#!/bin/bash
sed -i '1 a listeners=PLAINTEXT://0.0.0.0:9092' $KAFKA_HOME/config/server.properties
sed -i '1 a advertised.listeners=PLAINTEXT://localhost:9092' $KAFKA_HOME/config/server.properties

$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties &
 
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties &

$KAFKA_HOME/bin/kafka-topics.sh --create --topic location --replication-factor 1 --partitions 2 --bootstrap-server localhost:9092

$KAFKA_HOME/bin/kafka-server-stop.sh
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties
