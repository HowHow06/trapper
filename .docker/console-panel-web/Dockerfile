# Use an official Node.js runtime as the base image
FROM node:18-alpine


RUN mkdir /app/
# Set the working directory in the Docker image
WORKDIR /app

# Add the package.json and package-lock.json (if available) to the Docker image
COPY console-panel-web/package.json ./

# Install the application dependencies
RUN yarn

# Add the rest of the application code to the Docker image
COPY console-panel-web/ .

# Build the Next.js application
RUN yarn build

# Expose port 3000 in the Docker image
EXPOSE 3000

ENV NEXT_TELEMETRY_DISABLED 1
# Start the application
CMD ["yarn", "start"]



