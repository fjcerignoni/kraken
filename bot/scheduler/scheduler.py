#!/usr/bin/env python3
import os
from argparse import ArgumentParser
from datetime import datetime

from crontab import CronTab

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.environ.get('APP_DIR', os.path.join(BASE_DIR, '../..'))


def main():

    if args.debug:
        print('DEBUG mode')
        mem_cron = CronTab(tab=f"""
            * * * * * {APP_DIR}/.venv/bin/python {APP_DIR}/bot/scheduler/jobs.py
        """)
    else:
        mem_cron = CronTab(tab=f"""
            0 12 * * 0 {APP_DIR}/.venv/bin/python {APP_DIR}/bot/scheduler/jobs.py
        """)

    for result in mem_cron.run_scheduler():
        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\tDone')


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    main()