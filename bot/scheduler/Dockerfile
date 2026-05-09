FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.6.13 /uv /uvx /bin/

ENV APP_DIR=/opt/kraken
ENV LOG_DIR=/var/log/supervisor

RUN apt-get update && \
    apt-get install -y --no-install-recommends supervisor && \
    rm -rf /var/lib/apt/lists/*

WORKDIR $APP_DIR

COPY ./bot/scheduler ./bot/scheduler
COPY pyproject.toml uv.lock ./
COPY ./bot/scheduler/supervisord.conf ./supervisord.conf

RUN useradd -m -s /bin/bash kraken && \
    chown -R kraken:kraken $APP_DIR

RUN mkdir /var/run/supervisor && \
    chown -R kraken:kraken /var/run/supervisor && \
    chown -R kraken:kraken /var/log/supervisor

USER kraken

ENV PATH=$APP_DIR/.venv/bin:$PATH

RUN uv sync --frozen --no-dev

#CMD ["tail", "-f", "/dev/null"]
CMD ["supervisord", "-u", "kraken", "-c", "/opt/kraken/supervisord.conf"]