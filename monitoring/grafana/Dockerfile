from grafana/grafana:10.2.0

user root

copy grafana.ini /etc/grafana/grafana.ini

copy provisioning/ /etc/grafana/provisioning/

copy dashboards/ /var/lib/grafana/dashboards/

run chmod 644 /etc/grafana/grafana.ini && \
  chmod -R 644 /etc/grafana/provisioning/ && \
  chmod -R 644 /var/lib/grafana/dashboards/

expose 3000

user 472