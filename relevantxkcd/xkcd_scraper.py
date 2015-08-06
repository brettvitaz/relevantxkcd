import requests
import time

from sqlalchemy.sql.expression import func

from relevantxkcd.database import session_scope, Comic

URL = 'http://xkcd.com/{:d}/info.0.json'

complete = False


def get_all_the_things():
    """
    Download the xkcd comic metadata and store it in the configured database.
    """
    global complete
    complete = False

    print('Starting xkcd comic data downloader.')

    with session_scope() as session:
        query = session.query(func.max(Comic.num)).scalar()

    idx = query or 0
    if idx:
        print('Last comic number in database:', idx)

    while not complete:
        idx += 1

        # Skip some comics that intentionally cause a bad response. (Only 404 as of now.)
        if idx in [404]:
            idx += 1

        # Sometimes getting the response times out. Keep trying.
        response = None
        tries = 0
        while response is None or response.status_code != 200:
            if tries >= 5:
                print('Download failed. Aborting.')
                complete = True
                break

            tries += 1
            time.sleep(1.0)
            response = requests.get(URL.format(idx), timeout=5.0)

            if response.status_code != 200:
                print('Failed to download comic number: {:d}. Tried {:d} times. Response: {}'
                      .format(idx, tries, response.status_code))

            # A response code of 404 should indicate that there are no more comics available to download.
            if response.status_code == 404:
                complete = True
                break

        if not complete:
            print('Saving data for comic:', idx)
            # Gather only the items with keys we recognize.
            kwargs = {k: v for k, v in response.json().items() if k in Comic.__table__.columns}
            comic = Comic(**kwargs)
            with session_scope() as session:
                session.add(comic)

    print('Finished xkcd downloader.')


def shutdown(signum=None, frame=None):
    """
    Stop the download process, allowing the current job to complete.
    :param signum:
    :param frame:
    """
    global complete
    complete = True

    print('Shutting down downloader.')
