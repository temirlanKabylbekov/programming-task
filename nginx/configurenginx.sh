#!/bin/bash
echo "configuring nginx..."

app_server_host=$1
app_server_port=$2

cat > /etc/nginx/nginx.conf << EOF
user  nginx;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {
  worker_connections  1024;
}

http {
  include       /etc/nginx/mime.types;
  default_type  application/octet-stream;

  log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

  access_log  /var/log/nginx/access.log  main;

  sendfile        on;

  keepalive_timeout  65;

  upstream app {
    server $app_server_host:$app_server_port;
  }

  server {
    listen 80;
    charset utf-8;
    
    location = /favicon.ico {
        return 204;
        access_log     off;
        log_not_found  off;
    }

    location / {
        try_files \$uri @proxy_to_app;
    }

    location @proxy_to_app {
        proxy_redirect     off;
        proxy_set_header   Host \$host;
        proxy_set_header   X-Real-IP \$remote_addr;
        proxy_set_header   X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Host \$server_name;
        proxy_pass         http://app;
    }
  }
}
EOF

echo "nginx configured as:"
cat /etc/nginx/nginx.conf
