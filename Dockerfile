FROM registry.gitlab.com/namingthingsishard/net/torrent/libtorrent-docker as base

WORKDIR /app

RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        python3-pip \
        libboost-python1.74.0 \
    && rm -rf /var/cache/apt /var/lib/apt/lists/* \

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

FROM base as prod

COPY .  ./
ENTRYPOINT ["python3", "-m", "peertube_reseed"]

FROM base as dev

