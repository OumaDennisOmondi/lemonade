#!/usr/bin/env python3

import psutil
import time
import subprocess
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/laravel-monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LaravelMonitor:
    def __init__(self):
        self.cpu_threshold = 80.0  # 80% CPU threshold
        self.check_interval = 30   # Check every 30 seconds
        self.service_name = "laravel-monitor.service"  # Systemd service name
        
    def get_php_path(self):
        """Get PHP executable path"""
        try:
            result = subprocess.run(
                ["which", "php"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            logger.error("PHP not found in system PATH")
        return "/usr/bin/php"  # fallback to default    
    

    def get_cpu_usage(self):
        """Get current CPU usage percentage"""
        try:
            return psutil.cpu_percent(interval=1)
        except Exception as e:
            logger.error(f"Error getting CPU usage: {e}")
            return 0.0

    def restart_service(self):
        """Restart the Laravel service"""
        try:
            logger.info("Attempting to restart Laravel service...")
            php_path = self.get_php_path()
            logger.info(f"Using PHP at: {php_path}")
            
            # Run artisan down command first
            down = subprocess.run(
                [self.php_path, "artisan", "down"],
                cwd="/home/ubuntu/laravel-app",
                capture_output=True,  # Capture the output
                text=True,           # Return string instead of bytes
                check=True
            )
            if "maintenance" in down.stdout.lower():
                logger.info("Application brought down successfully")
            else:
                logger.error(f"Unexpected output: {down.stdout}")
                return False
            
            # Wait for service to start
            time.sleep(7)
            
            # Run artisan up command
            up = subprocess.run(
            [self.php_path, "artisan", "up"],
            cwd="/home/ubuntu/laravel-app",
            capture_output=True,  # Capture the output
            text=True,           # Return string instead of bytes
            check=True
            )
            
            if "live" in up.stdout.lower():
                logger.info("Laravel application restarted successfully")
                return True
            else:
                logger.error(f"Service restart failed - service not active : {up.stdout}")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to restart service: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during restart: {e}")
            return False

    def monitor(self):
        """Main monitoring loop"""
        logger.info("Starting Laravel service monitor...")
        
        while True:
            try:
                cpu_usage = self.get_cpu_usage()
                logger.debug(f"Current CPU usage: {cpu_usage}%")

                if cpu_usage >= self.cpu_threshold:
                    logger.warning(
                        f"High CPU usage detected: {cpu_usage}% "
                        f"(threshold: {self.cpu_threshold}%)"
                    )
                    
                    if self.restart_service():
                        # Add some cooldown period after restart
                        logger.info("Waiting 5 minutes before resuming monitoring...")
                        time.sleep(300)  # 5 minutes cooldown
                    else:
                        logger.error("Service restart failed, will retry in 60 seconds")
                        time.sleep(60)

                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    # Ensure script is running as root
    if os.geteuid() != 0:
        print("This script must be run as root!")
        exit(1)
        
    monitor = LaravelMonitor()
    monitor.monitor()