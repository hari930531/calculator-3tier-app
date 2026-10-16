# Use the official MySQL 8.0 base image from Docker Hub
FROM mysql:8.0

# Copy the custom database schema into MySQL's entrypoint initialization directory
# Files inside /docker-entrypoint-initdb.d/ are executed alphabetically on container first run
COPY database/init.sql /docker-entrypoint-initdb.d/init.sql

# Expose the default MySQL service port inside the container network
EXPOSE 3306