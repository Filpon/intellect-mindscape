# Use the official Grafana image
FROM grafana/grafana:latest

# Copy the dashboard configuration
COPY grafana/dashboards/dashboard.json /etc/grafana/provisioning/dashboards/dashboard.json

# Copy the Prometheus configuration
COPY prometheus.yml /etc/prometheus/prometheus.yml

# Copy the Loki configuration
COPY loki-config.yml /etc/loki/local-config.yaml

# Copy the Promtail configuration
COPY promtail-config.yml /etc/promtail/config.yaml

# Expose the necessary ports
EXPOSE 9090 3100