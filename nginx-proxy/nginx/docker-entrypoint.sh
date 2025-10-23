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

echo "Starting nginx..."

exec nginx -g 'daemon off;'