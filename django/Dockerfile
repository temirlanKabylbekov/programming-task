FROM python:3.6

ARG DB_HOST
ARG DB_PORT
ARG DB_WAIT_TIMEOUT
ARG DJANGO_PORT

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
            locales-all gettext netcat ca-certificates wget && \
    apt-get autoremove -y && \
    apt-get clean

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY . /django
WORKDIR /django

RUN pip install pip --upgrade && \
    pip install -r requirements/dev.txt --no-cache-dir

EXPOSE ${DJANGO_PORT}

CMD dockerize -wait tcp://${DB_HOST}:${DB_PORT} -timeout ${DB_WAIT_TIMEOUT} ./manage.py collectstatic --noinput && ./manage.py migrate && ./manage.py runserver 0.0.0.0:${DJANGO_PORT}
