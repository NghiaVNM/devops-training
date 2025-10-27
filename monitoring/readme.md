Prometheus + Grafana which export (node, DB, web) integrate with slack, email

# 1. MongoDB
docker build -t mongodb:1.0.0 .
docker run -d --name mongodb --network monitoring-network mongodb:1.0.0
# 2. Mongo Exporter
docker build -t mongo-exporter:1.0.0 .
docker run -d --name mongo-exporter --network monitoring-network --env-file .env mongo-exporter:1.0.0
# 3. Python web 2
docker build -t python-web-2:1.0.0 .
docker run -d --name python-web-2 --network monitoring-network python-web-2:1.0.0
# 4. Node Exporter
docker build -t node-exporter:1.0.0 .
docker run -d --name node-exporter --network monitoring-network -v "/:/host/rootfs:ro,rslave" -v "/proc:/host/proc:ro" -v "/sys:/host/sys:ro" node-exporter:1.0.0
# 5. Prometheus
docker build -t prometheus:1.0.0 .
docker run -d --name prometheus --network monitoring-network prometheus:1.0.0
# 6. Grafana
docker build -t grafana:1.0.0 .
docker run -d --name grafana --network monitoring-network grafana:1.0.0