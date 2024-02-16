# simple_bdp guide

NOTE: 

- **Docker images are for platform "linux/arm64" and tested in Mac M1**
- Docker-compose runs databse init for creating DB and tables

## Run 1 node

1. Build and run docker compose: ```bash run_compose_up_1dbnode.sh``` (NOTE: if network error occurs, run step 4 to tear down docker compose and wait a couple of minutes for network to reset)
2. Send test data: ```bash send_data_to_api.sh``` (NOTE: comment out other curl to send more data for testing)
3. Access Nifi: <a href="http://localhost:9443/nifi"> http://localhost:9443/nifi </a> for adjusting number of concurrency and debug
4. After testing, run ```bash run_compose_down_1dbnode.sh```

## Run 3 node (NOT IMPLEMENTed)

1. Build and run docker compose: ```bash run_compose_up_3dbnode.sh``` (NOTE: if network error occurs, run step 4 to tear down docker compose and wait a couple of minutes for network to reset)
2. Send test data: ```bash send_data_to_api.sh``` (NOTE: comment out other curl to send more data for testing)
3. Access Nifi: <a href="http://localhost:9443/nifi"> http://localhost:9443/nifi </a> for adjusting number of concurrency and debug
4. After testing, run ```bash run_compose_down_3dbnode.sh```

## Tear down
Finally, run ```bash prune.sh``` after finish testings

## Get logfile

```docker-compose -f docker-compose.1dbnode.yml logs -f -t >> logs/1dbnode-10concurrencenifi-2tables.log-docker-compose.yml.log```
