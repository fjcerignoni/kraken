FROM python:3.8

ENV APP_DIR=/opt/kraken
ENV LOG_DIR=/var/log/supervisor

RUN apt-get update && \
    apt-get install -y supervisor

WORKDIR $APP_DIR

COPY ./scheduler ./scheduler
COPY requirements.txt .
COPY supervisord.conf .

RUN useradd -m -s /bin/bash kraken && \
    chown -R kraken:kraken $APP_DIR

RUN mkdir /var/run/supervisor && \
    chown -R kraken:kraken /var/run/supervisor && \
    chown -R kraken:kraken /var/log/supervisor

USER kraken

RUN python3 -m venv --clear --copies .venv
ENV PATH=$APP_DIR/.venv/bin:$PATH

RUN python -m pip install --upgrade \
    pip \
    wheel \
    setuptools && \
    pip install -r requirements.txt

#CMD ["tail", "-f", "/dev/null"]
CMD ["supervisord", "-u", "kraken", "-c", "/opt/kraken/supervisord.conf"]