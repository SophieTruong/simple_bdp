#!/bin/bash
echo Wait for servers to be up
sleep 10

HOSTPARAMS="--host dbcockroach-1 --insecure"
SQL="./cockroach.sh sql $HOSTPARAMS"

$SQL -e "CREATE DATABASE IF NOT EXISTS airbnb_test;"
