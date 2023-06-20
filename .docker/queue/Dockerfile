# Dockerfile
FROM rabbitmq:3-management

# Add our entrypoint script
COPY rabbitmq-entrypoint.sh /rabbitmq-entrypoint.sh

RUN chmod +x /rabbitmq-entrypoint.sh

# Expose ports for AMQP, Management Interface
EXPOSE 5672 15672

# Use our script as the entrypoint
ENTRYPOINT ["/rabbitmq-entrypoint.sh"]