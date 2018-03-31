from flask import Flask
from datetime import datetime
from confluent_kafka import Producer
from datetime import datetime
from flask import request	
from flask import Response

import json

app = Flask(__name__)

@app.route("/order", methods=['POST'])
def order():
	data  = ""
	if request.method == 'POST':
		data = json.dumps(request.json)

		p = Producer({'bootstrap.servers': '127.0.0.1:29092'})
		p.produce('mytopic', data.encode('utf-8'))
		p.flush()

		return Response(data, status=200, mimetype='application/json')
	else:
		return Response({'message' : 'Invalid request'}, status=404, mimetype='application/json')

@app.route("/")
def hello():
    return "Hey I'm using Docker!"

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port=80)
