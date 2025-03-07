FROM python:3.8.3-alpine3.10
MAINTAINER Jose Gabriel Giron <jgabrielsk8@gmail.com>

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps

RUN mkdir /app
WORKDIR /app
COPY docker-requirements.txt /app/
RUN pip install -r docker-requirements.txt
EXPOSE 8000
COPY . /app/