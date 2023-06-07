FROM python:3.11

COPY . .

RUN make init
CMD make execute

EXPOSE 8000
