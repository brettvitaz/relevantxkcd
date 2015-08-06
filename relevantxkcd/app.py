import datetime
import signal
import sys

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from relevantxkcd import xkcd_scraper
from relevantxkcd.api.api_controller import ApiController
from relevantxkcd.database import database

import bottle
import waitress


class App:
    _scheduler = None
    _scraper_job = None

    def __init__(self):
        self._schedule_jobs()

        self._init_handle_shutdown()

        database.init_database()

    def _init_handle_shutdown(self):
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

    def shutdown(self, signum, frame):
        print('Shutting down application.')
        self._scheduler.shutdown()
        xkcd_scraper.shutdown()
        sys.exit(signum)

    def _schedule_jobs(self):
        self._scheduler = BackgroundScheduler()
        in_one_minute = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self._scraper_job = self._scheduler.add_job(xkcd_scraper.get_all_the_things, IntervalTrigger(days=1),
                                                    max_instances=1, next_run_time=in_one_minute)
        self._scheduler.start()

    def run(self):
        bottle_app = bottle.app()

        # Initialize the app context
        app_context = [ApiController()]

        # Serve the api
        waitress.serve(bottle_app, host='0.0.0.0', port=8080)
