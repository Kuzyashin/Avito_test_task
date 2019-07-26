FROM python:3.7.0-alpine3.8
MAINTAINER Alexey Kuzyashin <terr.kuzyashin@gmail.com>


COPY ./project /project

WORKDIR /project

RUN apk --update add python3 py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  && apk del build-dependencies



COPY ./docker/entrypoint.sh /entrypoint.sh


RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
