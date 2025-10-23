from node:18-alpine

run addgroup -S -g 1001 appuser && \
  adduser -S -u 1001 -G appuser appuser

run apk add --no-cache curl

workdir /app

copy app/package*.json ./

run npm install --only=production && \
  npm cache clean --force

copy app/ .

run chown -R appuser:appuser /app

user appuser

expose 80

healthcheck --interval=30s --timeout=3s --retries=3 \
  cmd curl -f http://localhost:80/healthz || exit 1

cmd ["node", "index.js"]