FROM python:3.8.5-slim-buster
LABEL org.opencontainers.image.source https://github.com/oakestra/schedulers

RUN mkdir /app
ADD requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt

ADD . /app

ENV RESOURCE_ABSTRACTOR_URL=localhost
ENV RESOURCE_ABSTRACTOR_PORT=10000

ENV REDIS_ADDR=redis://:clusterRedis@localhost:6379

ENV MY_PORT=10013
EXPOSE 10013

CMD celery -A scheduler.celeryapp worker --concurrency=1 --loglevel=INFO --uid=nobody --gid=nogroup
