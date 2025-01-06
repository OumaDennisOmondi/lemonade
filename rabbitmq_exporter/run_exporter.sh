#!/bin/bash

#install python3.12-venv
sudo apt-get install python3.12-venv -y

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

## Install requirements
pip install -r requirements.txt

# Set environment variables
export RABBITMQ_PROTOCOL=http
export RABBITMQ_HOST=localhost
export RABBITMQ_PORT=15672
export RABBITMQ_USER=admin
export RABBITMQ_PASSWORD=adminpass
export EXPORTER_PORT=8000

# Run the exporter
python3 rabbitmq_exporter.py