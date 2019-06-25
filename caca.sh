#!/bin/bash

docker-compose down
sudo rm -rf ./ACS/data
echo 'rm data done'
sudo rm -rf ./ACS/__pycache__
echo 'rm pycache done'
