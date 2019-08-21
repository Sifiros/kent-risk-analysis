#!/bin/bash

echo 'installing merchant dependencies'
cd ./Merchant/
npm install
echo 'Mooving into merchant front'
cd ./merchant-front-demo/
echo 'installing front dependencies'
npm install
echo 'starting react build'
npx react-scripts build

echo 'NPX DONE'

echo 'Moving back'
cd ..

echo 'Building docker'
docker-compose up
