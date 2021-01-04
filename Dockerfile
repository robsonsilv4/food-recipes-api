FROM python:3.9-alpine
LABEL author "Robson Silva"

ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache postgresql-client
RUN apk add --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user