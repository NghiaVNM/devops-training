from eclipse-temurin:17-jdk-alpine as build

workdir /app

copy app/src ./src

run javac -d /app/classes src/main/java/Main.java

from eclipse-temurin:17-jre-alpine

run addgroup -S -g 1001 appuser && \
    adduser -S -u 1001 -G appuser appuser

workdir /app

copy --from=build /app/classes ./classes

run apk add --no-cache curl

user appuser

expose 80

healthcheck --interval=30s --timeout=3s --retries=3 \
  cmd curl -f http://localhost:80/healthz || exit 1

cmd ["java", "-cp", "classes", "Main"]