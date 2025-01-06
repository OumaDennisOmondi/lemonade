# Instructions
### Task 1.Dockerize Laravel.
**Note**
Modify the production.ini, opcache.ini and www.ini to meet your optimization and perfomance needs accordingly
Modify the 'build.sh' to set ENV variables for DB, port etc.

1.Change directory to  ```laravel-docker```'
``` cd laravel-docker```
2.Make the script ```build.sh``` executable.
```chmod +x ./build.sh```
3.Execute the ```build.sh``` to build and run the container on the fly.
```./build.sh```

### Task 2. Script to restart the Laravel backend service if CPU usage exceeds 80%.
**Notes**
The script is wrritten in python.
The script is registered as a Unit of type Service, meaning it will run as a daemon in the backround and can be controlled by Systemd.(systemctl)
The service will restart automatically on OS boot/reboot and recover on failure.

**Steps**
1.Change directory to  ```laravel-restart```
``` cd laravel-restart```
2.Make the script ```build.sh``` executable
```chmod +x install.sh```
3.Execute the ```install.sh``` as sudo to.
```./install.sh``` 
The above will perfom the below operations
 - Install dependencies
 - Install the laravel-monitor as service
 - Enable and start the laravel-monitor service as a daemon
 
To check status of the service
``` systemctl status laravel-monitor.service```
To view logs
```tail -f /var/log/laravel-monitor.log```
To simulate, use stress tool like so
```sudo stress --cpu 8 --timeout 20```

### Task 3. Prometheus exporter in Python/Golang that connects to specified RabbitMQ

**Notes**
The exporter is wrritten in python.
Metrics should only be pulled from the application when Prometheus scrapes them, exporters should not perform scrapes based on their own timers. That is, all scrapes should be synchronous.
The exporter exposes metrics on ```localhost:8000/metrics``` by deafult.
CPU is checked every 5sec by default

The setup includes:
A sample producer to publish to queue, and a sample consumer for tests(```consumer.py & producer.py```)

**Steps**
1.Change directory to the 'rabbitmq_exporter'
``` cd rabbitmq_exporter```
2.Make the scripts ```run_exporter.sh``` and ```run_rabbitmq_docker.sh``` executable
```chmod +x run_exporter.sh run_rabbitmq_docker```

3.Start RabbitMQ in docker.
```./run_rabbitmq_docker.sh``` 
View the rabbitmq management console at ```localhost:15672```

4.Run the exporter.
```./run_exporter.sh``` 
To view the exposed metrics, go to ```localhost:8000/metrics```

**You can adjust the ENV accordingly.


