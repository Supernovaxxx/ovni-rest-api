FROM python:3.11.0-bullseye   

WORKDIR /opt

RUN groupadd -r CPops && useradd -r -g CPops CPops && chown -R CPops:CPops /opt
USER CPops

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /opt/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN make prepare 
RUN make init

CMD make execute

EXPOSE 8000
