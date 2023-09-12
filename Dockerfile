# Execution environment definition
#
# This files specifies how to build execution environment
# See https://docs.docker.com/engine/reference/builder/.


FROM python:3.11

ARG UID=1000
ARG GID=1000
ARG USER=user
ARG WORKDIR=/usr/src

ENV PYTHON '/usr/local/bin/python3'
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR $WORKDIR

RUN \
    groupadd --gid "${GID}" "${USER}" && \
    useradd \
    --gid "${GID}" \
    --uid "${UID}" \
    --system \
    "${USER}"

COPY Makefile requirements.txt ./
RUN make init
COPY . .

RUN chown -R $USER:$USER $WORKDIR
USER $USER

HEALTHCHECK CMD curl --fail http://localhost/ || exit 1

EXPOSE 8000
CMD ["make", "run"]
