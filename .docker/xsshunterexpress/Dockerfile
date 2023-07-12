FROM node:16-alpine

# Set up directory for the server
RUN mkdir /app/
# WORKDIR /app/

# Copy front-end over
# COPY xsshunter-express/front-end/ /app/front-end/
# WORKDIR /app/front-end/
# RUN npm install
# RUN npm run-script build

WORKDIR /app/
COPY xsshunter-express/package.json /app/
COPY xsshunter-express/package-lock.json /app/
RUN yarn

COPY xsshunter-express/server.js /app/
COPY xsshunter-express/probe.js /app/
COPY xsshunter-express/constants.js /app/
COPY xsshunter-express/notification.js /app/
COPY xsshunter-express/database.js /app/
COPY xsshunter-express/api.js /app/
COPY xsshunter-express/app.js /app/
COPY xsshunter-express/utils.js /app/
COPY xsshunter-express/templates /app/templates

COPY .docker/xsshunterexpress/docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 55000
# EXPOSE 443

# Start the server
ENTRYPOINT ["/app/docker-entrypoint.sh"]
