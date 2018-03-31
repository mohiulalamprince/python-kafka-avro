#FROM tiangolo/uwsgi-nginx-flask:flask
FROM tiangolo/uwsgi-nginx-flask:python2.7
RUN apt-get update -y

RUN apt-get install -y python-pip telnet

COPY ./app /app
WORKDIR /app

RUN curl -L https://github.com/edenhill/librdkafka/archive/v0.9.2-RC1.tar.gz | tar xzf - && \
cd librdkafka-0.9.2-RC1/ && \
./configure --prefix=/usr && \
make -j && \
make install

RUN pip install -r requirements.txt
