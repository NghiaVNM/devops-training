from golang:1.21-alpine as builder

workdir /build

copy app/go.mod ./
run go mod download

copy app/ .

run CGO_ENABLED=0 GOOS=linux go build -a --installsuffix cgo -o main .

from alpine:3.22

run addgroup -S -g 1001 appuser && \
  adduser -S -u 1001 -G appuser appuser

run apk add --no-cache curl

workdir /app

copy --from=builder /build/main .

run chown -R appuser:appuser /app

user appuser

expose 80

healthcheck --interval=30s --timeout=3s --retries=3 \
  cmd curl -f http://localhost:80/healthz || exit 1

cmd ["./main"]