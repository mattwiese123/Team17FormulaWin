#!/bin/bash

# Phase 1
sudo docker compose -f ./docker-compose-initiate.yml up -d nginx
sudo docker compose -f ./docker-compose-initiate.yml up certbot
sudo docker compose -f ./docker-compose-initiate.yml down

# letsencrypt
curl -L --create-dirs -o services/letsencrypt/options-ssl-nginx.conf https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf
openssl dhparam -out services/letsencrypt/ssl-dhparams.pem 2048

# Phase 2
sudo docker compose -f ./docker-compose.yml up -d --build
