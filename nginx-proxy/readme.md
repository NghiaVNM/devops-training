# Nginx Reverse Proxy for Multiple Web Applications

This project demonstrates an nginx reverse proxy setup that routes traffic to multiple web applications built with different programming languages (Python, Node.js, Go, Java, PHP, and Ruby).

## Architecture

- **nginx-proxy**: Acts as a reverse proxy and handles SSL/TLS certificates
- **python-web**: Python FastAPI application
- **nodejs-web**: Node.js application
- **golang-web**: Go application
- **java-web**: Java application
- **php-web**: PHP application
- **ruby-web**: Ruby application

All services communicate through a Docker bridge network (`nginx-proxy-network`).

## Prerequisites

- Docker
- Docker Compose

## Quick Start

### 1. Setup Environment Variables

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` and set your domain and email:

```bash
DOMAIN=your-domain.com
EMAIL=your-email@example.com
```

### 2. Run with Docker Compose

#### Development Mode (Local Build)

```bash
docker compose -f docker-compose.dev.yml up -d
```

#### Production Mode (Using Pre-built Images)

```bash
docker compose up -d
```

### 3. Verify Services

Check if all containers are running:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

## Manual Build & Run (Alternative)

If you prefer to build and run containers manually:

### Create Network

```bash
docker network create app-network
```

### Build and Run nginx-proxy

```bash
cd nginx
docker build -t nginx-proxy:1.0.0 .
docker run -d --name nginx-proxy -p 80:80 -p 443:443 --network app-network --env-file .env nginx-proxy:1.0.0
```

### Build and Run python-web

```bash
cd python-web
docker build -t python-web:1.0.0 .
docker run -d --name python-web --network app-network python-web:1.0.0
```

### Build and Run nodejs-web

```bash
cd nodejs-web
docker build -t nodejs-web:1.0.0 .
docker run -d --name nodejs-web --network app-network nodejs-web:1.0.0
```

### Build and Run golang-web

```bash
cd golang-web
docker build -t golang-web:1.0.0 .
docker run -d --name golang-web --network app-network golang-web:1.0.0
```

### Build and Run php-web

```bash
cd php-web
docker build -t php-web:1.0.0 .
docker run -d --name php-web --network app-network php-web:1.0.0
```

### Build and Run java-web

```bash
cd java-web
docker build -t java-web:1.0.0 .
docker run -d --name java-web --network app-network java-web:1.0.0
```

### Build and Run ruby-web

```bash
cd ruby-web
docker build -t ruby-web:1.0.0 .
docker run -d --name ruby-web --network app-network ruby-web:1.0.0
```

## Stopping Services

### With Docker Compose

```bash
docker compose down
```

### Manual Cleanup

```bash
docker stop nginx-proxy python-web nodejs-web golang-web php-web java-web ruby-web
docker rm nginx-proxy python-web nodejs-web golang-web php-web java-web ruby-web
docker network rm app-network
```

## Health Checks

All services include health checks accessible at `/healthz` endpoint:

- Python: `http://localhost/python/healthz`
- Node.js: `http://localhost/nodejs/healthz`
- Go: `http://localhost/golang/healthz`
- PHP: `http://localhost/php/healthz.php`
- Java: `http://localhost/java/healthz`
- Ruby: `http://localhost/ruby/healthz`

## Logs

Nginx logs are persisted to `./nginx_logs/` directory on the host machine.

## Security Features

- Non-root user execution in all containers
- Health checks for all services
- SSL/TLS support with Let's Encrypt
- Automatic certificate renewal

## License

This project is for training purposes.