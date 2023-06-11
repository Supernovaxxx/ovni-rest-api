FROM python:3.11

COPY requirements.txt /opt/app/requirements.txt

RUN make /opt/app

COPY . /opt/app

WORKDIR /opt/app

RUN make init
CMD make execute 

EXPOSE 8000
