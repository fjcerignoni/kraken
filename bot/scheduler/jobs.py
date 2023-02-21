#!/usr/bin/env python3
import logging
import os
import urllib.request

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.environ.get('APP_DIR', os.path.join(BASE_DIR, '../..'))
LOG_DIR = os.environ.get('LOG_DIR', os.path.join(APP_DIR, 'bot', 'scheduler', 'logs'))


def main():
    get_items()


def get_items():

    url = "https://raw.githubusercontent.com/broderickhyman/ao-bin-dumps/master/formatted/items.json"

    try:
        with urllib.request.urlopen(url) as src:
            with open(os.path.join(APP_DIR, 'bot', 'db', 'items.json'), 'w',
                      encoding='utf-8') as file:
                file.write(src.read().decode())

        logging.info('Dados sobre itens atualizados com sucesso')
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s\t%(levelname)s\t%(message)s",
        filename=os.path.join(LOG_DIR, 'jobs.log'),
        filemode='a'
    )

    main()