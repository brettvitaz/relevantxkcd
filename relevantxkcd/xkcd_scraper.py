import requests
import time
import sys

from sqlalchemy.sql.expression import func

from relevantxkcd.database import Session, Comic

URL = 'http://xkcd.com/{:d}/info.0.json'


def get_all_the_things():
    session = Session()

    try:
        query = session.query(func.max(Comic.num)).scalar()
        idx = query or 0
        print('Starting with comic number:', idx)
    except:
        session.rollback()
        raise
    finally:
        session.close()

    complete = False

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
                print('Download failed. Aborting')
                sys.exit(1)

            tries += 1
            time.sleep(1.0)
            response = requests.get(URL.format(idx), timeout=5.0)

            if response.status_code != 200:
                print('Failed to download comic number: {:d}. Tried {:d} times. Response: {}'
                      .format(idx, tries, response.status_code))

            # A response code of 404 should indicate that there are no more comics available to download.
            if response.status_code == 404:
                print('Finished')
                complete = True
                break

        if not complete:
            # Gather only the items with keys we recognize.
            kwargs = {k: v for k, v in response.json().items() if k in Comic.__table__.columns}
            comic = Comic(**kwargs)
            try:
                session.add(comic)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
