from percona/mongodb_exporter:0.40

expose 9216

healthcheck --interval=30s --timeout=10s --start-period=5s --retries=3 \
  cmd wget --quiet --tries=1 --spider http://localhost:9216/metrics || exit 1