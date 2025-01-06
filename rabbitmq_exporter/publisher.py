import pika
import json
import random
import time
from datetime import datetime

def connect_to_rabbitmq():
    credentials = pika.PlainCredentials('admin', 'adminpass')
    parameters = pika.ConnectionParameters(
        host='localhost',
        port=5672,
        credentials=credentials
    )
    return pika.BlockingConnection(parameters)

def publish_messages(queue_name, num_messages=10):
    try:
        # Establish connection
        connection = connect_to_rabbitmq()
        channel = connection.channel()

        # Declare queue
        channel.queue_declare(queue=queue_name, durable=True)

        # Publish messages
        for i in range(num_messages):
            message = {
                'message_id': i,
                'timestamp': datetime.now().isoformat(),
                'data': f'Test message {i}',
                'value': random.randint(1, 100)
            }
            
            channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                )
            )
            print(f"Published message {i} to queue {queue_name}")
            time.sleep(0.5)  # Small delay between messages

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection and not connection.is_closed:
            connection.close()

if __name__ == "__main__":
    publish_messages('test_queue', 20)