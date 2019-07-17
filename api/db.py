from datetime import datetime as dt
import names
import asyncpgsa
from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, DateTime, desc
)
from sqlalchemy.dialects.postgresql import JSONB


class RecordNotFound(Exception):
    """Requested record in database was not found"""


metadata = MetaData()

groups = Table(
   'groups', metadata,

   Column('id', Integer, primary_key=True),
   Column('title', String(64), nullable=False),
   Column('date_created', DateTime, index=True, default=dt.utcnow),

   Column('data', JSONB, nullable=False),
)


async def init_db(app):
    dsn = construct_db_url(app['config'])
    pool = await asyncpgsa.create_pool(dsn=dsn)
    app['db_pool'] = pool


async def close_db(app):
    await app['db_pool'].close()


def construct_db_url(config):
    DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
    return DSN.format(
        user=config['DB_USER'],
        password=config['DB_PASS'],
        database=config['DB_NAME'],
        host=config['DB_HOST'],
        port=config['DB_PORT'],
    )


async def get_last_group(conn):
    records = await conn.fetch(
        groups.select().order_by(desc(groups.c.date_created)).limit(1)
    )
    return records


async def get_all_groups(conn):
    records = await conn.fetch(
        groups.select().order_by()
    )
    return records


async def get_group_by_id(conn, group_id):
    group = await conn.fetch(
        groups.select().where(groups.c.id == group_id)
    )
    return group


async def create_data(conn, data):
    stmt = groups.insert().values(
        title=names.get_full_name(),
        data=data['data'],
    )
    await conn.execute(stmt)
