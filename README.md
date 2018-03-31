## Install virtual box from internet
## Then vagrant and I am using mac

vagrant init ubuntu/xenial:64
vagrant up
vagrant ssh

## environment setup for kafka python
sudo apt-get update -y
sudp apt-get install docker.io

docker run -d -p 6379:6379 -t redis:latest
docker run --name postgres-container -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres

sudo apt-get install python-pip -y
sudo apt-get install python-dev -y

sudo apt-get install build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev libssl-dev -y

sudo easy_install greenlet -y
sudo easy_install gevent -y


## install docker compose
sudo curl -L https://github.com/docker/compose/releases/download/1.20.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

cd cp-docker-images/examples/kafka-single-node
sudo docker-compose up

## you need to install rdkafka for your kafka python development
curl -L https://github.com/edenhill/librdkafka/archive/v0.9.2-RC1.tar.gz | tar xzf -
cd librdkafka-0.9.2-RC1/
./configure --prefix=/usr
make -j
sudo make install

## docker image

git clone https://github.com/confluentinc/cp-docker-images
cp *.py cp-docker-images/example/kafka-single-node/


## create a kafka topic using docker command
sudo docker-compose exec kafka  \
kafka-topics --create --topic mytopic --partitions 1 --replication-factor 1 --if-not-exists --zookeeper localhost:32181


## check the status/description
sudo docker-compose exec kafka  \
  kafka-topics --describe --topic mytopic --zookeeper localhost:32181


## generate some messages 
sudo docker-compose exec kafka  \
  bash -c "seq 42 | kafka-console-producer --request-required-acks 1 --broker-list localhost:29092 --topic mytopic && echo 'Produced 42 messages.'"

## consume some message what you have ever pushed in kafka mytopic
sudo docker-compose exec kafka  \
  kafka-console-consumer --bootstrap-server localhost:29092 --topic mytopic --from-beginning --max-messages 42  


## need to install virtualenv for python development
sudo pip install virtualenv
virtualenv env

## activate your environment
source env/bin/activate


## install confluent kafka for your development
pip install confluent-kafka


## Lets see what can be done with this two sample code
python producer.py
python consumer.py

(env) vagrant@ubuntu-xenial:~$ time python producer.py 

real    0m0.727s
user    0m0.184s
sys     0m0.036s


## kafka schema registry using docker container
sudo docker run -d \
  --net=host \
  --name=schema-registry \
  -e SCHEMA_REGISTRY_KAFKASTORE_CONNECTION_URL=localhost:32181 \
  -e SCHEMA_REGISTRY_HOST_NAME=localhost \
  -e SCHEMA_REGISTRY_LISTENERS=http://localhost:8081 \
  confluentinc/cp-schema-registry:4.0.0  

## mysql installation
sudo docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:5.6


## REST api apps
mkdir docker-flask-project && cd docker-flask-project
touch Dockerfile 

paste inside Docker file 
'
FROM tiangolo/uwsgi-nginx-flask:flask


RUN apt-get update -y                                                                                                                                           [1/517]
                                                                                                                                                                       
RUN apt-get install -y python-pip telnet

COPY ./app /app
WORKDIR /app

RUN curl -L https://github.com/edenhill/librdkafka/archive/v0.9.2-RC1.tar.gz | tar xzf - && \
cd librdkafka-0.9.2-RC1/ && \
./configure --prefix=/usr && \
make -j && \
make install

RUN pip install -r requirements.txt
'

## REST api using flask
sudo docker build -t simple-flask .
sudo docker run -p 80:80 -t simple-flask 


## how to run kafka using docker not docker-compose
sudo docker run -d \
    --net=host \
    --name=kafka \
    -e KAFKA_ZOOKEEPER_CONNECT=localhost:32181 \
    -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:29092 \
    -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
    confluentinc/cp-kafka:4.0.0

sudo docker run -d \
    --net=host \
    --name=zookeeper \
    -e ZOOKEEPER_CLIENT_PORT=32181 \
    confluentinc/cp-zookeeper:4.0.0

sudo docker run \
  --net=host \
  --rm confluentinc/cp-kafka:4.0.0 \
  kafka-topics --create --topic mytopic --partitions 1 --replication-factor 1 --if-not-exists --zookeeper localhost:32181

sudo docker run \
  --net=host \
  --rm confluentinc/cp-kafka:4.0.0 \
  kafka-topics --create --topic mytopic --partitions 1 --replication-factor 1 --if-not-exists --zookeeper localhost:32181

sudo docker run \
  --net=host \
  --rm \
  confluentinc/cp-kafka:4.0.0 \
  kafka-topics --describe --topic mytopic --zookeeper localhost:32181
## MYSQL 

sudo docker --name db -e MYSQL_ROOT_PASSWORD=test -d -p 3306:3306 mariadb
sudo docker run --name mysql-client -it --link db:mysql --rm mariadb sh -c 'exec mysql -uroot -ptest -hmysql'

show databases;

create database testdb;

use testdb;

show tables;

MariaDB [testdb]> create table shipmentorder(order_id INT NOT NULL AUTO_INCREMENT, orderstatus VARCHAR(64) NOT NULL, PRIMARY KEY(order_id));

## How to run the flask app from the console

cd docker-flask-project/app/
flask run


## How to run the consumer
source env/bin/activate
cd docker-flask-project/app
python consumer

## How to check the basic features

curl 127.0.0.1:5000
curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/order -d '{"orderstatus":"shipped"}'


