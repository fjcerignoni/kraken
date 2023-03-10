FROM python:3.8

ENV APP_DIR=/opt/kraken
ENV DB_DIR=$APP_DIR/bot/db

RUN apt-get update && \
    apt-get install -y locales locales-all && \
    apt-get install -y sqlite3 libsqlite3-dev

WORKDIR $APP_DIR

COPY ./bot ./bot
COPY requirements.txt .

RUN useradd -m -s /bin/bash kraken && \
    chown -R kraken:kraken $APP_DIR

USER kraken

RUN python3 -m venv --clear --copies .venv
ENV PATH=$APP_DIR/.venv/bin:$PATH

RUN python -m pip install --upgrade pip wheel && \
              pip install -r requirements.txt

RUN if [ -f $DB_DIR/kraken.sqlite ]; then echo "database ok"; else sqlite3 $DB_DIR/kraken.sqlite < $DB_DIR/kraken_schema.sql; fi
RUN if [ -f $DB_DIR/items.json ]; then echo "items list ok"; else python $APP_DIR/bot/scheduler/jobs.py; fi

CMD ["python", "/opt/kraken/bot/main.py"]
