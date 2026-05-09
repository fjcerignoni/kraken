FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.6.13 /uv /uvx /bin/

ENV APP_DIR=/opt/kraken
ENV DB_DIR=$APP_DIR/bot/db

RUN apt-get update && \
    apt-get install -y --no-install-recommends locales locales-all sqlite3 libsqlite3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR $APP_DIR

COPY ./bot ./bot
COPY pyproject.toml uv.lock ./

RUN useradd -m -s /bin/bash kraken && \
    chown -R kraken:kraken $APP_DIR

USER kraken

ENV PATH=$APP_DIR/.venv/bin:$PATH

RUN uv sync --frozen --no-dev

RUN if [ -f $DB_DIR/kraken.sqlite ]; then echo "database ok"; else sqlite3 $DB_DIR/kraken.sqlite < $DB_DIR/kraken_schema.sql; fi
RUN if [ -f $DB_DIR/items.json ]; then echo "items list ok"; else python $APP_DIR/bot/scheduler/jobs.py; fi

CMD ["python", "/opt/kraken/bot/main.py"]
