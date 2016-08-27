# Collectd Docker Stats Plugin

Simple and solid collectd plugin that listens for docker stats, fetches and enriches them and sends them to the configured backend of choice

The following stats will be reported for each container

- Network bandwidth
- Memory usage percentage
- CPU usage percentage
- Block IO

Only unique stats will be reported per container, global stats like ```memory.limit``` will be reported together for all containers to avoid overhead

Each metric is send as a single value to achieve maximum backend compability

### Setup

- Clone this repository ```git clone https://github.com/21stio/collectd-docker-stats-plugin.git /opt/collectd-docker-stats-plugin```
- Install python dependencies ```pip install -r requirements.txt```
- Configure the plugin, see [collectd.conf](collectd.conf)
- Restart collectd

### Testing

Only ```docker-compose``` is required to execute the tests

```
docker-compose up style
docker-compose up unit-test
docker-compose up integration-test_docker
docker-compose up integration-test_collectd
```

```docker-compose up integration-test_collectd``` will create a ```stats``` folder and place the collectd stats in it

To run an integration test against the backend of interest adapt [collectd.conf](collectd.conf) and run ```docker-compose up integration-test_collectd-custom``` and interupt the execution once you checked your backend

### Requirements
- docker-py
- python-dateutil
- docker 1.5+

### Credits

Inspired by ```https://github.com/lebauce/docker-collectd-plugin```
