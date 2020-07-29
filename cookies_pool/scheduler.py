"""Schedule jobs."""
from multiprocessing import Pool

from .generator import FBCookiesGenerator, IGCookiesGenerator
from .settings import (
    GENERATOR_MAP,
    GENERATOR_PROCESS_ENABLED,
    TESTER_MAP,
    TESTER_PROCESS_ENABLED
)
from .tester import FBCookiesTester, IGCookiesTester


class Context:
    """Execute strategy from client."""

    def __init__(self, strategy):
        """Initialize."""
        self.strategy = strategy

    def execute_strategy(self):
        """Delegate real strategy."""
        self.strategy.run()


class Scheduler:
    """Wrap for Scheduler."""

    @staticmethod
    def generator_client(cond: str):
        """Generator client.

        Args:
            cond (str): website name, e.g. 'fb', 'ig'
        """
        if cond == 'facebook':
            context = Context(FBCookiesGenerator(website='fb'))
        elif cond == 'instagram':
            context = Context(IGCookiesGenerator(website='ig'))
        context.execute_strategy()

    @staticmethod
    def tester_client(cond: str):
        """Tester client.

        Args:
            cond (str): website name, e.g. 'fb', 'ig'
        """
        if cond == 'facebook':
            context = Context(FBCookiesTester(website='fb'))
        elif cond == 'instagram':
            context = Context(IGCookiesTester(website='ig'))
        context.execute_strategy()

    def run(self):
        """Execute task."""
        pool = Pool(processes=3)
        if GENERATOR_PROCESS_ENABLED:
            pool.map(Scheduler.generator_client, GENERATOR_MAP)
        if TESTER_PROCESS_ENABLED:
            pool.map(Scheduler.tester_client, TESTER_MAP)
        pool.close()
        pool.join()
