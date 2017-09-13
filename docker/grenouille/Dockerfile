FROM sinet/nginx-node:latest

COPY docker/grenouille/default.conf /etc/nginx/conf.d/

# Install and build the application
COPY . /grenouille/
WORKDIR /grenouille/frontend
RUN npm install \
	&& npm run build

