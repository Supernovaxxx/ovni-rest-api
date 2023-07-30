FROM python:3.12.0b3

ENV PYTHONUNBUFFERED 1
ARG WORKDIR=/opt
WORKDIR $WORKDIR

COPY requirements.txt Makefile ${WORKDIR}
RUN make init
COPY . .

RUN groupadd -r USERapp \
    && useradd -r -g USERapp USERapp

RUN chown -R USERapp:USERapp $WORKDIR
USER USERapp

EXPOSE 8000

CMD make execute