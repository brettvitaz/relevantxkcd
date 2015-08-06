from contextlib import contextmanager

from alembic import command, config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_URL = 'sqlite:///relevantxkcd.sqlite'

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)

Base = declarative_base()

alembic_config = config.Config('./alembic.ini')


def init_database():
    with engine.connect() as connection:
        alembic_config.attributes['connection'] = connection
        command.upgrade(alembic_config, 'head')


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
