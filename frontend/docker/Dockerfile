# Use a specific version of Nginx
FROM nginx:1.25.2

# Copy the build output to replace the default nginx contents.
COPY ./dist /usr/share/nginx/html

# Copy the Nginx configuration file
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
