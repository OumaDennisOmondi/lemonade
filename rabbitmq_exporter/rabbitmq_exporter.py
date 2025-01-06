from prometheus_client import start_http_server, REGISTRY
from prometheus_client.core import GaugeMetricFamily, CollectorRegistry
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os
import logging
import signal
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('rabbitmq_exporter')

class RabbitMQCollector:
    def __init__(self):
        # Add HTTPS and port configuration
        protocol = os.environ.get('RABBITMQ_PROTOCOL', 'http')
        port = os.environ.get('RABBITMQ_PORT', '15672')
        self.host = os.environ.get('RABBITMQ_HOST', 'localhost')
        self.user = os.environ.get('RABBITMQ_USER', 'guest')
        self.password = os.environ.get('RABBITMQ_PASSWORD', 'guest')
        self.base_url = f'{protocol}://{self.host}:{port}/api'
        
        # Improve retry strategy with connect timeouts
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"],  # Only retry GET requests
            raise_on_status=True
        )
        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def get_queue_data(self):
        """Fetch queue data from RabbitMQ with retry logic"""
        try:
            response = self.session.get(
                f'{self.base_url}/queues',
                auth=(self.user, self.password),
                timeout=(3, 5)  # (connect timeout, read timeout)
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch queue data: {str(e)}")
            return None

    def collect(self):
        """Collection method that Prometheus calls to gather metrics"""
        # Define metric families with detailed help text
        metric_families = {
            'messages': GaugeMetricFamily(
                'rabbitmq_individual_queue_messages',
                'Total number of messages currently in the queue, including ready and unacknowledged messages',
                labels=['host', 'vhost', 'name']
            ),
            'messages_ready': GaugeMetricFamily(
                'rabbitmq_individual_queue_messages_ready',
                'Number of messages ready to be delivered to consumers',
                labels=['host', 'vhost', 'name']
            ),
            'messages_unacked': GaugeMetricFamily(
                'rabbitmq_individual_queue_messages_unacknowledged',
                'Number of messages delivered to consumers but not yet acknowledged',
                labels=['host', 'vhost', 'name']
            )
        }

        # Fetch queue data
        queues = self.get_queue_data()
        
        if queues is None:
            logger.error("No queue data available to export")
            # Still yield empty metrics to avoid breaking the scrape
            for metric in metric_families.values():
                yield metric
            return

        # Process each queue
        for queue in queues:
            try:
                labels = [self.host, queue['vhost'], queue['name']]
                
                metric_families['messages'].add_metric(labels, queue['messages'])
                metric_families['messages_ready'].add_metric(labels, queue['messages_ready'])
                metric_families['messages_unacked'].add_metric(labels, queue['messages_unacknowledged'])
                
            except KeyError as e:
                logger.error(f"Missing expected field in queue data: {str(e)}")
                continue

        # Yield all metrics
        for metric in metric_families.values():
            yield metric

def main():
    try:
        # Create and register collector
        registry = CollectorRegistry()
        registry.register(RabbitMQCollector())
        
        # Start server on configured port
        port = int(os.environ.get('EXPORTER_PORT', '8000'))
        start_http_server(port, registry=registry)
        logger.info(f"RabbitMQ exporter started on port {port}")
        
        # Improved signal handling for graceful shutdown
        def signal_handler(signum, frame):
            logger.info("Received shutdown signal, exiting...")
            exit(0)
            
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        signal.pause()
        
    except Exception as e:
        logger.error(f"Failed to start exporter: {str(e)}", exc_info=True)
        raise

if __name__ == '__main__':
    main()