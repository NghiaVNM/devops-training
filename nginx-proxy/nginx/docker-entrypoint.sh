#!/bin/sh
set -e

if [ -d "/etc/nginx/templates" ]; then
  echo "Processing nginx templates..."
  for template in /etc/nginx/templates/*.template; do
    if [ -f "$template" ]; then
      filename=$(basename "$template" .template)
      envsubst '$DOMAIN' < "$template" > "/etc/nginx/conf.d/$filename"
      echo "Processed: $filename"
    fi
  done
fi

mkdir -p /var/www/certbot
if [ ! -f "/etc/letencrypt/live/${DOMAIN}/fullchain.pem" ]; then
  echo "SSL certificate not found. Obtaining certificates..."

  echo "Starting nginx temporarily for certificate validation..."

  for conf in /etc/nginx/conf.d/*.conf; do
    sed -i '/server {/,/}/{ /listen 443/,/^}/d; }' "$conf" 2>/dev/null || true
  done

  nginx

  sleep 2

  certbot certonly --webroot \
    -w /var/www/certbot \
    -d ${DOMAIN} \
    -d python.${DOMAIN} \
    -d nodejs.${DOMAIN} \
    -d golang.${DOMAIN} \
    -d php.${DOMAIN} \
    -d java.${DOMAIN} \
    -d ruby.${DOMAIN} \
    --email ${EMAIL} \
    --agree-tos \
    --non-interactive \
    --quiet || {
      echo "Failed to obtain certificates"
      exit 1
    }
  
  nginx -s stop
  sleep 2

  echo "Restoring SSL configurations..."
    for template in /etc/nginx/templates/*.template; do
      if [ -f "$template" ]; then
        filename=$(basename "$template" .template)
        envsubst '$DOMAIN' < "$template" > "/etc/nginx/conf.d/$filename"
      fi
    done

  echo "SSL certificates obtained successfully!"
else
  echo "SSL certificates found."
fi

echo "Starting nginx..."
exec nginx -g 'daemon off;'