from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.engine.url import URL

from settings import DB_CONFIG
from settings import ENGINE_PARAMETERS
from db import users


def create_tables(engine):
    """Drops specified tables and creates them anew."""

    meta = MetaData()
    meta.drop_all(bind=engine, tables=[users])
    meta.create_all(bind=engine, tables=[users])


if __name__ == "__main__":
    engine = create_engine(URL(**DB_CONFIG),
                           **ENGINE_PARAMETERS)
    create_tables(engine)
