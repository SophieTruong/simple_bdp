echo killing old docker processes
docker-compose rm -fs

echo building docker containers
docker-compose up -V --build -d

# Source: https://docker-docs.uclv.cu/compose/reference/up/
# -V: Recreate anonymous volumes instead of retrieving data from the previous containers.