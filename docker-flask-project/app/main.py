from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route("/order")
def order():
    return str(datetime.utcnow())

@app.route("/")
def hello():
    return "Hey I'm using Docker!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)