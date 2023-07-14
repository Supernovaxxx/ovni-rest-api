FROM python:3.12.0b3 AS build

WORKDIR /tmp

COPY requirements.txt Makefile /tmp/
RUN apt update \
    && make init
COPY . .

FROM python:3.12.0b3

RUN mkdir -p /home/app \
    && groupadd -r USERapp \
    && useradd -r -g USERapp USERapp

ENV HOME=/home/app
WORKDIR $HOME

COPY --from=build /tmp/requirements.txt .
COPY --from=build /tmp/Makefile .
COPY --from=build /tmp .

ENV PYTHONUNBUFFERED 1
EXPOSE 8000

RUN chown -R USERapp:USERapp $HOME
USER USERapp

CMD make execute