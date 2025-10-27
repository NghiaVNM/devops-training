from prom/prometheus:v2.47.2

copy prometheus.yml /etc/prometheus/prometheus.yml

expose 9090

cmd ["--config.file=/etc/prometheus/prometheus.yml", \
  "--storage.tsdb.path=/prometheus", \
  "--web.console.libraries=/etc/prometheus/console_libraries", \
  "--storage.tsdb.retention.time=200h", \
  "--web.enable-lifecycle"]