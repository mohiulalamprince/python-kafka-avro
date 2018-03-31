from confluent_kafka import Consumer, KafkaError
from EmailManager import send_email
from sqlalchemy import create_engine
from datetime import datetime

import json

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
    
    ## redundant call
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break
    send_email("", "", msg.value)
    print('Received message: {}'.format(msg.value().decode('utf-8')))
   
    data = "" 
    try:
	print "writing inside mysql"
    	engine = create_engine("mysql+pymysql://root:test@localhost/testdb?host=localhost?port=3306")
    	conn = engine.connect()
    	conn.execute('insert into shipmentorder values(0, "' + str(datetime.utcnow()) + '")')
	conn.close()
	print "writing end inside mysql"
    except:
	print "exception inside mysql" + str(data)

c.close()
