from alembic import command, config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DB_URL = 'sqlite:///relevantxkcd.sqlite'

alembic_config = config.Config('./alembic.ini')

engine = create_engine(DB_URL, echo=True)

Base = declarative_base()


def init_database():
    with engine.connect() as connection:
        alembic_config.attributes['connection'] = connection
        command.upgrade(alembic_config, 'head')
