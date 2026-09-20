FROM docker.elastic.co/logstash/logstash:8.13.0

# JDBC input plugin (ships logstash-integration-jdbc, but re-install pins the version).
RUN logstash-plugin install logstash-integration-jdbc

# Postgres JDBC driver. Version must match the one referenced as
# jdbc_driver_library in pipeline/logstash.conf.
# Downloaded at build time so the image is self-contained.
RUN curl -sSL -o /usr/share/logstash/logstash-core/lib/jars/postgresql-42.7.3.jar \
      https://jdbc.postgresql.org/download/postgresql-42.7.3.jar && \
    ls -la /usr/share/logstash/logstash-core/lib/jars/postgresql-42.7.3.jar

# NOTE (no network at build time? alternative):
# 1. Download manually: curl -O https://jdbc.postgresql.org/download/postgresql-42.7.3.jar
# 2. Place it next to this Dockerfile and replace the RUN above with:
#      COPY postgresql-42.7.3.jar /usr/share/logstash/logstash-core/lib/jars/
