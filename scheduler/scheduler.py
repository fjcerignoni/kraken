#!/usr/bin/env python3
import os
from crontab import CronTab

#APP_DIR = os.path.join('/opt', 'kraken')
APP_DIR = os.environ.get('APP_DIR', os.path.join('/mnt', 'f', 'git', 'kraken'))


def main():

    mem_cron = CronTab(tab=f"""
        * * * * * {APP_DIR}/.venv/bin/python {APP_DIR}/scheduler/jobs.py
    """)

    for result in mem_cron.run_scheduler():
        print('rodou')


if __name__ == '__main__':
    main()