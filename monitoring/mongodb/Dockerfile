from mongo:7.0

copy init-mongo.js /docker-entrypoint-initdb.d/

expose 27017

cmd ["mongod","--auth", "--bind_ip_all"]