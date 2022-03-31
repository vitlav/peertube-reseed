FROM registry.gitlab.com/namingthingsishard/net/torrent/libtorrent-docker

WORKDIR /app

RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        python3-pip \
    && rm -rf /var/cache/apt /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "-m", "peertube_reseed"]

COPY .  ./
