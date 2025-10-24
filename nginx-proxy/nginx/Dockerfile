from nginx:1.29-alpine

run addgroup -S -g 1001 web && adduser -S -u 1001 -G web web

run apk add --no-cache certbot certbot-nginx gettext curl

copy nginx.conf /etc/nginx/nginx.conf
copy conf.d/ /etc/nginx/templates/
copy docker-entrypoint.sh /docker-entrypoint.sh
copy certbot-renew.sh /etc/periodic/daily/certbot-renew

run mkdir -p /var/cache/nginx /var/run/nginx /var/log/nginx /etc/letsencrypt \
  && chown -R web:web /var/cache/nginx /var/run/nginx /var/log/nginx

run chmod +x /docker-entrypoint.sh /etc/periodic/daily/certbot-renew

healthcheck --interval=30s --timeout=3s --retries=3 \
  CMD curl -fsS http://localhost:80/healthz || exit 1

stopsignal sigquit

expose 80 443

env DOMAIN=localhost
env EMAIL=admin@example.com

entrypoint ["/docker-entrypoint.sh"]