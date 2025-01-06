# Instructions
### Task 1.Dockerize Laravel.<br>
**Note**<br>
Modify the production.ini, opcache.ini and www.ini to meet your optimization and perfomance needs accordingly<br>
Modify the 'build.sh' to set ENV variables for DB, port etc.<br>

1.Change directory to  ```laravel-docker```' <br>
``` cd laravel-docker```<br>
2.Make the script ```build.sh``` executable.<br>
```chmod +x ./build.sh```<br>
3.Execute the ```build.sh``` to build and run the container on the fly.<br>
```./build.sh```<br>

### Task 2. Script to restart the Laravel backend service if CPU usage exceeds 80%.<br>
**Notes**<br>
The script is wrritten in python.<br>
The script is registered as a Unit of type Service, meaning it will run as a daemon in the backround and can be controlled by Systemd.(systemctl)<br>
The service will restart automatically on OS boot/reboot and recover on failure.<br>

**Steps**<br>
1.Change directory to  ```laravel-restart```<br>
``` cd laravel-restart```<br>
2.Make the script ```build.sh``` executable<br>
```chmod +x install.sh```<br>
3.Execute the ```install.sh``` as sudo to.<br>
```./install.sh``` <br>
The above will perfom the below operations<br>
 - Install dependencies<br>
 - Install the laravel-monitor as service<br>
 - Enable and start the laravel-monitor service as a daemon<br>
 
To check status of the service<br>
``` systemctl status laravel-monitor.service```<br>
To view logs<br>
```tail -f /var/log/laravel-monitor.log```<br>
To simulate, use stress tool like so<br>
```sudo stress --cpu 8 --timeout 20```<br>

### Task 3. Prometheus exporter in Python/Golang that connects to specified RabbitMQ

**Notes**<br>
The exporter is wrritten in python.<br>
Metrics should only be pulled from the application when Prometheus scrapes them, exporters should not perform scrapes based on their own timers. That is, all scrapes should be synchronous.<br>
The exporter exposes metrics on ```localhost:8000/metrics``` by deafult.<br>
CPU is checked every 5sec by default<br>

The setup includes:<br>
A sample producer to publish to queue, and a sample consumer for tests(```consumer.py & producer.py```)<br>

**Steps**
1.Change directory to the 'rabbitmq_exporter'<br>
``` cd rabbitmq_exporter```<br>
2.Make the scripts ```run_exporter.sh``` and ```run_rabbitmq_docker.sh``` executable<br>
```chmod +x run_exporter.sh run_rabbitmq_docker```<br>

3.Start RabbitMQ in docker.<br>
```./run_rabbitmq_docker.sh``` <br>
View the rabbitmq management console at ```localhost:15672```<br>

4.Run the exporter.<br>
```./run_exporter.sh``` <br>
To view the exposed metrics, go to ```localhost:8000/metrics```<br>

**You can adjust the ENV accordingly.


