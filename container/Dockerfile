# Dockerfile - Spark with additional Python libraries and JDBC drivers
FROM apache/spark:3.5.1
USER root

# Install Python data science libraries
RUN pip install --no-cache-dir \
    pandas \
    numpy \
    pyarrow \
    delta-spark

# Add PostgreSQL JDBC driver for database connectivity
ADD https://jdbc.postgresql.org/download/postgresql-42.7.1.jar /opt/spark/jars/

USER spark