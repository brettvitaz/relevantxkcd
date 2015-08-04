from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from relevantxkcd import xkcd_scraper
from relevantxkcd.database import database


class App:
    _scheduler = None
    _scraper_job = None

    def __init__(self):
        self._scheduler = BackgroundScheduler()
        self._scheduler.start()
        self._schedule_jobs()

        database.init_database()

    def _schedule_jobs(self):
        self._scraper_job = self._scheduler.add_job(print, IntervalTrigger(days=1), ('hello',))

    def run(self):
        xkcd_scraper.get_all_the_things()
