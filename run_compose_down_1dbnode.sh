echo run docker-compose down
docker compose -f docker-compose.1dbnode.yml down --remove-orphans --volumes

# echo killing old docker processes
# docker-compose rm -fs
