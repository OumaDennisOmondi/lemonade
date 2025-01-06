# Create network if not exists
docker network create rabbitmq-net

# Run RabbitMQ with management plugin explicitly enabled
docker run -d \
    --name rabbitmq \
    --network rabbitmq-net \
    -p 5672:5672 \
    -p 15672:15672 \
    -e RABBITMQ_DEFAULT_USER=admin \
    -e RABBITMQ_DEFAULT_PASS=adminpass \
    rabbitmq:3-management \
    bash -c "rabbitmq-plugins enable rabbitmq_management && rabbitmq-server"