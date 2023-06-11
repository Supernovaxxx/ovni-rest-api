FROM python:3.11

COPY requirements.txt /tmp/

RUN cd /tmp/ \
    make prepare \
    make clean

COPY . /opt/
WORKDIR /opt
RUN make init 

EXPOSE 8000
