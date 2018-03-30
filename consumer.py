from confluent_kafka import Consumer, KafkaError


c = Consumer({
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'mygroup',
    'default.topic.config': {
        'auto.offset.reset': 'smallest'
    }
})

c.subscribe(['mytopic'])

while True:
    msg = c.poll()

    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break

    print('Received message: {}'.format(msg.value().decode('utf-8')))

c.close()
