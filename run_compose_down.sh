echo run docker-compose down
docker compose down --remove-orphans --volumes

echo killing old docker processes
docker-compose rm -fs
