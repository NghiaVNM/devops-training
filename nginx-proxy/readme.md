nginx proxy for multiple web

# 1. build
## 1.1. nginx-proxy
sh ```
docker build -t nginx-proxy:1.0.0 .
```

sh ```
docker run -d --name nginx-proxy -p 80:80 -p 443:443 --network app-network --env-file .env nginx-proxy:1.0.0
```
## 1.2. python-web
sh ```
docker build -t python-web:1.0.0 .
```
sh ```
docker run -d --name python-web --network app-network python-web:1.0.0
```
## 1.3. nodejs-web
sh ```
docker build -t nodejs-web:1.0.0 .
```
sh ```
docker run -d --name nodejs-web --network app-network nodejs-web:1.0.0
```
## 1.4. golang-web
sh ```
docker build -t golang-web:1.0.0 .
```
sh ```
docker run -d --name golang-web --network app-network golang-web:1.0.0
```
## 1.5. php-web
sh ```
docker build -t php-web:1.0.0 .
```
sh ```
docker run -d --name php-web --network app-network php-web:1.0.0
```
## 1.6. java-web
sh ```
docker build -t java-web:1.0.0 .
```
sh ```
docker run -d --name java-web --network app-network java-web:1.0.0
```
## 1.7. ruby-web
sh ```
docker build -t ruby-web:1.0.0 .
```
sh ```
docker run -d --name ruby-web --network app-network ruby-web:1.0.0
```