from confluent_kafka import Producer
from datetime import datetime
some_data_source = ['hello world1', 'hello world2', 'hello world3', 'hello world4', str(datetime.utcnow())]

for t in range(50000):
	some_data_source.append(str(datetime.utcnow()))

p = Producer({'bootstrap.servers': 'localhost:29092'})

for data in some_data_source:
    p.produce('mytopic', data.encode('utf-8'))

p.flush()
