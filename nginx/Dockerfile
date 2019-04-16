FROM nginx

ARG DJANGO_HOST
ARG DJANGO_PORT
ARG DJANGO_WAIT_TIMEOUT

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
            ca-certificates wget && \
    apt-get autoremove -y && \
    apt-get clean

ENV DOCKERIZE_VERSION v0.6.1
RUN wget http://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY configurenginx.sh /opt/install/configurenginx.sh
RUN chmod +x /opt/install/configurenginx.sh && ./opt/install/configurenginx.sh ${DJANGO_HOST} ${DJANGO_PORT}

EXPOSE ${NGINX_PORT}

CMD dockerize -wait tcp://${DJANGO_HOST}:${DJANGO_PORT} -timeout ${DJANGO_WAIT_TIMEOUT} nginx -g "daemon off;"
