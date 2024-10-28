FROM python:3.9

RUN mkdir /chat

WORKDIR /chat

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /chat/docker/*.sh

