FROM node:12-alpine

RUN apk add --no-cache bash npm

WORKDIR /www
COPY package.json /www
RUN npm install

COPY . /www
WORKDIR /www/merchant-front-demo
RUN npm install
RUN npx react-scripts build

WORKDIR /www
ENTRYPOINT ["npm", "start"]
