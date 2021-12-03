FROM node:16-slim as base

WORKDIR /app

RUN apt-get update -qq \
    && apt-get install -yqq \
        xvfb \
        chromium \
        git

COPY package*.json ./
RUN npm install --no-dev

ENTRYPOINT [ "npm", "start" ]

FROM base as prod

COPY .  ./

FROM base as dev

RUN npm install
