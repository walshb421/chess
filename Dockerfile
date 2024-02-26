FROM node:20 

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY vite.config.js .
COPY index.html .
COPY public public
COPY src src

CMD npm run dev

