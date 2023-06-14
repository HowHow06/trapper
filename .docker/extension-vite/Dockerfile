# Choose a base image that includes Node.js
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY extension-vite/package*.json ./

# Install dependencies
RUN yarn

# Copy source files
COPY extension-vite/ .

# Expose the port that Vite uses
EXPOSE 5000

# Run the app, use --debug to print, use --host to enable access from host OS to the machine in docker
CMD [ "yarn", "dev", "--debug", "--host" ] 
