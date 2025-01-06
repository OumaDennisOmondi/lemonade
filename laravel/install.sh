#!/bin/bash

# Check if the user is root
if [ "$EUID" -ne 0 ]
then
  echo "Please run as root"
  exit 1
fi

# Function to handle errors
handle_error() {
    echo "[ERROR] $1"
    exit 1
}

# install psutil globally
sudo apt install python3-psutil

# Copy the script to a suitable location and check if it succeeds
echo "Copying restart.py to /usr/local/bin/"
sudo cp restart.py /usr/local/bin/ || handle_error "Failed to copy restart.py to /usr/local/bin/"
sudo chmod +x /usr/local/bin/restart.py || handle_error "Failed to make restart.py executable"

# Create log file and check if it succeeds
echo "Creating log file /var/log/laravel-monitor.log"
sudo touch /var/log/laravel-monitor.log || handle_error "Failed to create /var/log/laravel-monitor.log"
sudo chmod 644 /var/log/laravel-monitor.log || handle_error "Failed to set permissions for /var/log/laravel-monitor.log"

# Copy the service file to the systemd directory and check if it succeeds
echo "Copying laravel-monitor.service to /etc/systemd/system/"
sudo cp laravel-monitor.service /etc/systemd/system/ || handle_error "Failed to copy laravel-monitor.service to /etc/systemd/system/"

# Reload systemd to recognize the new service
echo "Reloading systemd daemon"
sudo systemctl daemon-reload || handle_error "Failed to reload systemd daemon"

# Start the service and check if it succeeds
echo "Starting laravel-monitor service"
sudo systemctl start laravel-monitor || handle_error "Failed to start laravel-monitor service"

# Enable the service to start on boot
echo "Enabling laravel-monitor service to start on boot"
sudo systemctl enable laravel-monitor || handle_error "Failed to enable laravel-monitor service"

# Check the service status
echo "Checking laravel-monitor service status"
sudo systemctl status laravel-monitor || handle_error "Failed to get status of laravel-monitor service"

# Success message
echo "Setup completed successfully!"
