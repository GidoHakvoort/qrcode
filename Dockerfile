FROM python:3.7-alpine

RUN apk update \
    && apk add zlib-dev \
    && apk add jpeg-dev \
    && apk add libjpeg \
    && apk add gcc \
    && apk add musl-dev

RUN mkdir /app

WORKDIR /app

ADD requirements.txt /app

ADD main.py /app

RUN pip3 install -r requirements.txt

CMD ["gunicorn", "-w 2", "-b", "0.0.0.0:8000", "main:app"]