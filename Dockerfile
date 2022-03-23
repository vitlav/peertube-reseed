FROM python:3.10-slim as base

WORKDIR /app

RUN pip install poetry
COPY requirements.txt ./
RUN npm install --no-dev

ENTRYPOINT [ "npm", "start" ]

FROM base as prod

COPY .  ./

FROM base as dev

RUN npm install
