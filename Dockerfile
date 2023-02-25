FROM python:3.8

ENV APP_DIR=/opt/kraken

RUN apt-get update && \
    apt-get install -y locales locales-all

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

CMD ["python", "/opt/kraken/bot/main.py"]