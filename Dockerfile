FROM node:20 as vite 

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm ci

COPY vite.config.js .
COPY index.html .
COPY public public
COPY src src

CMD npm run dev

FROM python:3 as engine

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY engine/ ./

CMD [ "python", "./app.py" ]