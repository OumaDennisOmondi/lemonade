import pika
import json
import time
from datetime import datetime
import signal
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MessageConsumer:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.should_continue = True
        self.message_count = 0
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

    def handle_signal(self, signum, frame):
        logger.info("Received stop signal. Stopping gracefully...")
        self.should_continue = False
        sys.exit()

    def connect(self):
        credentials = pika.PlainCredentials('admin', 'adminpass')
        parameters = pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        )
        return pika.BlockingConnection(parameters)

    def process_message(self, ch, method, properties, body):
        """Process the received message"""
        try:
            message = json.loads(body)
            self.message_count += 1
            
            logger.info(f"Received message #{self.message_count}: {message}")
            
            # Simulate some processing time
            time.sleep(0.5)
            
            # Acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except json.JSONDecodeError:
            logger.error(f"Failed to parse message: {body}")
            # Negative acknowledgment for invalid messages
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            # Negative acknowledgment with requeue for other errors
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def start_consuming(self):
        try:
            connection = self.connect()
            channel = connection.channel()
            
            # Declare queue
            channel.queue_declare(queue=self.queue_name, durable=True)
            
            # Set QoS (prefetch count)
            channel.basic_qos(prefetch_count=1)
            
            # Setup consumer
            channel.basic_consume(
                queue=self.queue_name,
                on_message_callback=self.process_message
            )
            
            logger.info(f"Starting to consume messages from queue '{self.queue_name}'")
            logger.info("Press CTRL+C to stop")
            
            # Start consuming
            while self.should_continue:
                try:
                    channel.start_consuming()
                except pika.exceptions.AMQPChannelError as e:
                    logger.error(f"Channel error: {e}")
                    break
                except pika.exceptions.AMQPConnectionError as e:
                    logger.error(f"Connection error: {e}")
                    time.sleep(5)  # Wait before reconnecting
                    connection = self.connect()
                    channel = connection.channel()

        except KeyboardInterrupt:
            logger.info("Stopping consumer...")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            if connection and not connection.is_closed:
                connection.close()
            logger.info(f"Consumed total of {self.message_count} messages")


if __name__ == "__main__":
    consumer = MessageConsumer('test_queue')
    
    try:
        consumer.start_consuming()
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
        