from ruby:3.2-alpine

run addgroup -S -g 1001 appuser && \
  adduser -S -u 1001 -G appuser appuser

run apk add --no-cache --virtual .build-deps \
  build-base \
  && apk add --no-cache curl

workdir /app

copy app/Gemfile* ./

run bundle install --without development test && \
  bundle clean --force && \
  apk del .build-deps

copy app/ .

run apk add --no-cache curl && \
  chown -R appuser:appuser /app

user appuser

expose 80

healthcheck --interval=30s --timeout=3s --retries=3 \
  cmd curl -f http://localhost:80/healthz || exit 1

cmd ["ruby", "server.rb"]