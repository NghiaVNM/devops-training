from nginx:1.29-alpine

run addgroup -S -g 1001 web && adduser -S -u 1001 -G web web

copy nginx.conf /etc/nginx/nginx.conf
copy conf.d/ /etc/nginx/templates/
copy docker-entrypoint.sh /docker-entrypoint.sh

run mkdir -p /var/cache/nginx /var/run/nginx /var/log/nginx \
  && chown -R web:web /var/cache/nginx /var/run/nginx /var/log/nginx

run apk add --no-cache curl gettext

run chmod +x /docker-entrypoint.sh

healthcheck --interval=30s --timeout=3s --retries=3 \
  CMD curl -fsS http://localhost:80/healthz || exit 1

stopsignal sigquit

expose 80

env DOMAIN=localhost

entrypoint ["/docker-entrypoint.sh"]