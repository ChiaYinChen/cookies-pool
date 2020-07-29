"""Cookies-Pool process."""
import logging
import os

from cookies_pool.scheduler import Scheduler
from cookies_pool.utils import timer


@timer
def main():
    """Execute."""
    s = Scheduler()
    s.run()


if __name__ == '__main__':
    logging.info(f'Run the main process (pid: {os.getpid()})')
    logging.info('Process start')
    main()
    logging.info('Process end')
