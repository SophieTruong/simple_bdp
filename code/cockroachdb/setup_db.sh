#!/bin/bash
echo Wait for servers to be up
sleep 10

cockroach.sh sql --insecure \
--user=root \
-f airbnb_db.sql
