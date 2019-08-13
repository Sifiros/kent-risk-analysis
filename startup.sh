#!/bin/bash

echo 'Mooving into merchant front'
cd ./Merchant/merchant-front-demo/
echo 'starting react build'
npx react-scripts build

echo 'NPX DONE'



echo 'Mooving back'
cd ...

echo 'Building docker'
docker-compose up
