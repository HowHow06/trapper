#!/bin/sh
if [ $# != 2 ]; then
  echo "[Entrypoint] Warning: Please pass two parameters, which are admin username and admin password respectively"
  exit
fi
username=$1
password=$2

# Start RabbitMQ in the background
echo "[Entrypoint] Starting RabbitMQ in the background..."
rabbitmq-server -detached

# Function to wait for RabbitMQ startup
wait_for_start() {
  echo "[Entrypoint] Waiting for RabbitMQ startup..."
  while true; do
    if rabbitmqctl status; then
      return 0
    fi
    echo "[Entrypoint] Still waiting for RabbitMQ startup..."
    sleep 5s
  done
  echo "[Entrypoint] RabbitMQ startup failed"
  return 1
}

create_rabbitmq_admin_account() {
  echo "[Entrypoint] Creating RabbitMQ user and setting permissions..."
  rabbitmqctl add_user $username $password
  rabbitmqctl set_user_tags $username administrator
  rabbitmqctl set_permissions -p / $username ".*" ".*" ".*"
}

# Function to enable rabbitmq plugins
enable_rabbitmq_plugins() {
  echo "[Entrypoint] Enabling RabbitMQ plugins..."
  #   rabbitmq-plugins enable --offline rabbitmq_management # macam not needed
}

create_rabbitmq_exchange() {
  echo "[Entrypoint] Creating RabbitMQ exchanges..."
  rabbitmqadmin -u $username -p $password declare exchange name=trapper_fanout_exchange type=fanout

}

# Function to set up queues, exchanges, and bindings
create_rabbitmq_queues() {
  echo "[Entrypoint] Creating RabbitMQ queues..."
  rabbitmqadmin -u $username -p $password declare queue name=trapper-xsstrike
  # rabbitmqadmin -u $username -p $password declare queue name=trapper-xsstrike-test # for testing fanout exchange, it works
}

bind_rabbitmq_exchange() {
  echo "[Entrypoint] Binding RabbitMQ exchange to queue..."
  rabbitmqadmin -u $username -p $password declare binding source=trapper_fanout_exchange destination=trapper-xsstrike
  # rabbitmqadmin -u $username -p $password declare binding source=trapper_fanout_exchange destination=trapper-xsstrike-test  # for testing fanout exchange, it works

}

# Run the above functions
wait_for_start
echo "[Entrypoint] -> rabbitmq-server running"

create_rabbitmq_admin_account
enable_rabbitmq_plugins
create_rabbitmq_exchange
create_rabbitmq_queues
bind_rabbitmq_exchange

# Now stop the server and run it in the foreground
echo "[Entrypoint] Stopping RabbitMQ..."
rabbitmqctl stop

echo "[Entrypoint] Starting RabbitMQ in the foreground..." # if no process runnning in foreground, docker container will stop
rabbitmq-server
