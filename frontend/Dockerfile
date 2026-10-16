# Use a lightweight Nginx web server base image based on Alpine Linux
FROM nginx:alpine

# Copy all static assets (HTML, CSS, JS) directly into Nginx's default public web root
COPY . /usr/share/nginx/html

# Expose HTTP port 80 to receive web traffic
EXPOSE 80

# Run Nginx in the foreground so the Docker container remains active
CMD ["nginx", "-g", "daemon off;"]