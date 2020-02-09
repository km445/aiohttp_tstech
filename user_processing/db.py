from sqlalchemy import MetaData
from sqlalchemy import Sequence
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
import aiomysql.sa

from settings import DB_CONFIG
from settings import ENGINE_PARAMETERS

meta = MetaData()

users = Table(
    "users", meta,
    Column("id", Integer, Sequence('user_id_seq'), primary_key=True),
    Column("name", String(255), nullable=False),
    Column("age", Integer, nullable=False),
    Column("city", String(255), nullable=False))


async def init_mysql(app):
    engine = await aiomysql.sa.create_engine(
        db=DB_CONFIG["database"],
        user=DB_CONFIG["username"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        maxsize=ENGINE_PARAMETERS["pool_size"])
    app["db"] = engine


async def close_mysql(app):
    app["db"].close()
    await app["db"].wait_closed()
