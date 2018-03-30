###Install virtual box from internet
###Then vagrant and I am using mac

vagrant init ubuntu/xenial:64
vagrant up
vagrant ssh

###environment setup for kafka python
sudo apt-get update -y
sudp apt-get install docker.io

docker run -d -p 6379:6379 -t redis:latest
docker run --name postgres-container -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres

sudo apt-get install python-pip -y
sudo apt-get install python-dev -y

sudo apt-get install build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev libssl-dev -y

sudo easy_install greenlet -y
sudo easy_install gevent -y


###install docker compose
sudo curl -L https://github.com/docker/compose/releases/download/1.20.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

cd cp-docker-images/examples/kafka-single-node
sudo docker-compose up

###you need to install rdkafka for your kafka python development
curl -L https://github.com/edenhill/librdkafka/archive/v0.9.2-RC1.tar.gz | tar xzf -
cd librdkafka-0.9.2-RC1/
./configure --prefix=/usr
make -j
sudo make install


###create a kafka topic using docker command
sudo docker-compose exec kafka  \
kafka-topics --create --topic mytopic --partitions 1 --replication-factor 1 --if-not-exists --zookeeper localhost:32181


###check the status/description
sudo docker-compose exec kafka  \
  kafka-topics --describe --topic mytopic --zookeeper localhost:32181


###generate some messages 
sudo docker-compose exec kafka  \
  bash -c "seq 42 | kafka-console-producer --request-required-acks 1 --broker-list localhost:29092 --topic mytopic && echo 'Produced 42 messages.'"

###consume some message what you have ever pushed in kafka mytopic
sudo docker-compose exec kafka  \
  kafka-console-consumer --bootstrap-server localhost:29092 --topic mytopic --from-beginning --max-messages 42  


###need to install virtualenv for python development
sudo pip install virtualenv
virtualenv env

###activate your environment
source env/bin/activate


###install confluent kafka for your development
pip install confluent-kafka


###Lets see what can be done with this two sample code
python producer.py
python consumer.py

(env) vagrant@ubuntu-xenial:~$ time python producer.py 

real    0m0.727s
user    0m0.184s
sys     0m0.036s


###kafka schema registry using docker container
sudo docker run -d \
  --net=host \
  --name=schema-registry \
  -e SCHEMA_REGISTRY_KAFKASTORE_CONNECTION_URL=localhost:32181 \
  -e SCHEMA_REGISTRY_HOST_NAME=localhost \
  -e SCHEMA_REGISTRY_LISTENERS=http://localhost:8081 \
  confluentinc/cp-schema-registry:4.0.0  

 
