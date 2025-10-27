from prom/node-exporter:v1.6.1

expose 9100

cmd ["--path.procfs=/host/proc", \
  "--path.rootfs=/host/rootfs", \
  "--path.sysfs=/host/sys", \
  "--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)", \
  "--web.listen-address=:9100"]